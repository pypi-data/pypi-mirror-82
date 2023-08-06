import copy
import datetime
import json
import logging
import os
from packaging import version
import re
import shutil
import subprocess
import sys
import tempfile
from typing import Any, Dict, List, Optional, Tuple

import click
from ray.autoscaler.sdk import get_head_node_ip

# TODO(ilr) Remove this
from ray.autoscaler._private.commands import rsync
from ray.autoscaler._private.constants import DOCKER_MOUNT_PREFIX

import anyscale.legacy_projects as ray_scripts

import ray.ray_constants
import ray.scripts.scripts as autoscaler_scripts
import yaml

from anyscale.api import get_api_client, instantiate_api_client
from anyscale.auth_proxy import app as auth_proxy_app
from anyscale.autosync_heartbeat import managed_autosync_session
from anyscale.client.openapi_client.rest import ApiException  # type: ignore
from anyscale.cloudgateway import CloudGatewayRunner
from anyscale.cluster_config import (
    configure_for_session,
    get_cluster_config,
)
from anyscale.commands.cloud_commands import cloud_cli
from anyscale.commands.exec_commands import anyscale_exec
from anyscale.commands.list_commands import list_cli
from anyscale.commands.session_commands import anyscale_stop
import anyscale.conf
from anyscale.project import (
    ANYSCALE_AUTOSCALER_FILE,
    ANYSCALE_PROJECT_FILE,
    get_project_id,
    get_project_session,
    load_project_or_throw,
    ProjectDefinition,
    validate_project_name,
)
from anyscale.snapshot import (
    copy_file,
    describe_snapshot,
    get_snapshot_id,
)
from anyscale.util import (
    deserialize_datetime,
    execution_log_name,
    format_api_exception,
    get_container_name,
    get_endpoint,
    get_project_directory_name,
    get_rsync_command,
    get_working_dir,
    populate_session_args,
    send_json_request,
    send_json_request_raw,
    slugify,
    wait_for_session_start,
)


logging.basicConfig(format=ray.ray_constants.LOGGER_FORMAT)
logger = logging.getLogger(__file__)
logging.getLogger("botocore").setLevel(logging.CRITICAL)

if anyscale.conf.AWS_PROFILE is not None:
    logger.info("Using AWS profile %s", anyscale.conf.AWS_PROFILE)
    os.environ["AWS_PROFILE"] = anyscale.conf.AWS_PROFILE


class AliasedGroup(click.Group):
    # This is from https://stackoverflow.com/questions/46641928/python-click-multiple-command-names
    def get_command(self, ctx: Any, cmd_name: str) -> Any:
        try:
            cmd_name = ALIASES[cmd_name].name
        except KeyError:
            pass
        return super().get_command(ctx, cmd_name)


def get_user_cloud() -> Any:
    response = send_json_request("/api/v2/clouds/", {})
    clouds = response["results"]
    if len(clouds) > 1:
        raise click.ClickException(
            "Multiple clouds: {}\n"
            "Please specify the one you want to refer to.".format(
                [cloud["name"] for cloud in clouds]
            )
        )

    return clouds[0]


@click.group(
    invoke_without_command=True,
    no_args_is_help=True,
    cls=AliasedGroup,
    context_settings=dict(help_option_names=["-h", "--help"]),
)
@click.option(
    "--version",
    "-v",
    "version_flag",
    is_flag=True,
    default=False,
    help="Current anyscale version.",
)
@click.option(
    "--json",
    "show_json",
    is_flag=True,
    default=False,
    help="Return output as json, for use with --version.",
)
@click.pass_context
def cli(ctx: Any, version_flag: bool, show_json: bool) -> None:
    try:
        api_instance = instantiate_api_client(no_cli_token=True)
        resp = api_instance.get_anyscale_version_api_v2_userinfo_anyscale_version_get()
        curr_version = anyscale.__version__
        latest_version = resp.result.version
        if version.parse(curr_version) < version.parse(latest_version):
            message = "Warning: Using version {0} of anyscale. Please update the package using pip install anyscale -U to get the latest version {1}".format(
                curr_version, latest_version
            )
            print("\033[91m{}\033[00m".format(message), file=sys.stderr)
    except Exception as e:
        if type(e) == ApiException:
            logger.warning(
                "Error {} while trying to get latest anyscale version number: {}".format(
                    e.status, e.reason  # type: ignore
                )
            )
        else:
            logger.warning(e)

    if version_flag:
        ctx.invoke(version_cli, show_json=show_json)


@click.group("project", help="Commands for working with projects.", hidden=True)
def project_cli() -> None:
    pass


@click.group("session", help="Commands for working with sessions.", hidden=True)
def session_cli() -> None:
    pass


@click.group("snapshot", help="Commands for working with snapshot.", hidden=True)
def snapshot_cli() -> None:
    pass


@click.command(name="version", help="Display version of the anyscale CLI.")
@click.option(
    "--json", "show_json", is_flag=True, default=False, help="Return output as json."
)
def version_cli(show_json: bool) -> None:
    if show_json:
        print(json.dumps({"version": anyscale.__version__}))
    else:
        print(anyscale.__version__)


@cli.command(
    name="help", help="Display help documentation for anyscale CLI.", hidden=True
)
@click.pass_context
def anyscale_help(ctx: Any) -> None:
    print(ctx.parent.get_help())


def validate_cluster_configuration(
    cluster_config_file_name: str,
    cluster_config: Optional[Any] = None,
    api_instance: Optional[Any] = None,
) -> None:
    if not os.path.isfile(cluster_config_file_name):
        raise click.ClickException(
            "The configuration file {} does not exist. Please provide a valid config file.".format(
                cluster_config_file_name
            )
        )

    if not cluster_config:
        try:
            with open(cluster_config_file_name) as f:
                cluster_config = yaml.safe_load(f)
        except (ValueError, yaml.YAMLError):
            raise click.ClickException(
                "\tThe configuration file {} does not have a valid format. "
                "\n\tPlease look at https://github.com/ray-project/ray/blob/master/python/ray/autoscaler/aws/example-full.yaml "
                "for an example configuration file.".format(cluster_config_file_name)
            )

    if api_instance:
        try:
            api_instance.validate_cluster_api_v2_sessions_validate_cluster_post(
                body={"config": json.dumps(cluster_config)}
            )
        except ApiException as e:
            error = json.loads(json.loads(e.body)["error"]["detail"])
            path = ".".join(error["path"])
            if error["path"]:
                formatted_error = 'Error occured at "{k}: {v}" because {message}.\nSchema description for {k}:\n{schema}'.format(
                    k=path,
                    v=error["instance"],
                    message=error["message"],
                    schema=json.dumps(error["schema"], indent=4, sort_keys=True),
                )
            else:
                formatted_error = 'Error occured at "{v}" because {message}.\nSchema description:\n{schema}'.format(
                    v=error["instance"],
                    message=error["message"],
                    schema=json.dumps(error["schema"], indent=4, sort_keys=True),
                )
            raise click.ClickException(
                "The configuration file {0} is not valid.\n{1}".format(
                    cluster_config_file_name, formatted_error
                )
            )
    else:
        try:
            send_json_request(
                "/api/v2/sessions/validate_cluster",
                {"config": json.dumps(cluster_config)},
                method="POST",
            )
        except click.ClickException as e:
            try:
                error = json.loads(json.loads(e.message[5:-1])["error"]["detail"])
                path = ".".join(error["path"])
                if error["path"]:
                    formatted_error = 'Error occured at "{k}: {v}" because {message}.\nSchema description for {k}:\n{schema}'.format(
                        k=path,
                        v=error["instance"],
                        message=error["message"],
                        schema=json.dumps(error["schema"], indent=4, sort_keys=True),
                    )
                else:
                    formatted_error = 'Error occured at "{v}" because {message}.\nSchema description:\n{schema}'.format(
                        v=error["instance"],
                        message=error["message"],
                        schema=json.dumps(error["schema"], indent=4, sort_keys=True),
                    )
            except Exception as e_inner:
                raise click.ClickException("Error parsing exception.\n{}".format(e))

            raise click.ClickException(
                "The configuration file {0} is not valid.\n{1}".format(
                    cluster_config_file_name, formatted_error
                )
            )


def register_project(
    project_definition: ProjectDefinition, api_instance: Optional[Any] = None
) -> None:
    validate_cluster_configuration(
        project_definition.cluster_yaml(), api_instance=api_instance
    )

    project_name = project_definition.config["name"]
    description = project_definition.config.get("description", "")

    with open(project_definition.cluster_yaml(), "r") as f:
        initial_cluster_config = yaml.load(f, Loader=yaml.SafeLoader)

    # Add a database entry for the new Project.
    if api_instance:
        with format_api_exception(ApiException):
            resp = api_instance.create_project_api_v2_projects_post(
                write_project={
                    "name": project_name,
                    "description": description,
                    "initial_cluster_config": json.dumps(initial_cluster_config),
                }
            )
        result = resp.result
        project_id = result.id
    else:
        resp = send_json_request(
            "/api/v2/projects/",
            {
                "name": project_name,
                "description": description,
                "initial_cluster_config": json.dumps(initial_cluster_config),
            },
            method="POST",
        )
        result = resp["result"]
        project_id = result["id"]

    with open(anyscale.project.ANYSCALE_PROJECT_FILE, "w") as f:
        yaml.dump({"project_id": project_id}, f)

    # Print success message
    url = get_endpoint(f"/projects/{project_id}")
    print(f"Project {project_id} created. View at {url}")


def create_new_proj_def(
    name: Optional[str],
    cluster_config_file: Optional[str],
    api_instance: Optional[Any] = None,
) -> Tuple[str, ProjectDefinition]:
    project_name = ""
    if not name:
        while project_name == "":
            project_name = click.prompt("Project name", type=str)
            if not validate_project_name(project_name):
                print(
                    '"{}" contains spaces. Please enter a project name without spaces'.format(
                        project_name
                    ),
                    file=sys.stderr,
                )
                project_name = ""
        if not cluster_config_file:
            # TODO (yiran): Print cluster.yaml path in the else case.
            cluster_config_file = click.prompt(
                "Cluster yaml file (optional)",
                type=click.Path(exists=True),
                default=".",
                show_default=False,
            )
            if cluster_config_file == ".":
                # handling default value from prompt
                cluster_config_file = None
    else:
        project_name = str(name)
    if slugify(project_name) != project_name:
        project_name = slugify(project_name)
        print("Normalized project name to {}".format(project_name))

    # Create startup.yaml.
    if cluster_config_file:
        validate_cluster_configuration(cluster_config_file, api_instance=api_instance)
        if not os.path.exists(
            anyscale.project.ANYSCALE_AUTOSCALER_FILE
        ) or not os.path.samefile(
            cluster_config_file, anyscale.project.ANYSCALE_AUTOSCALER_FILE
        ):
            shutil.copyfile(
                cluster_config_file, anyscale.project.ANYSCALE_AUTOSCALER_FILE
            )
    else:
        if not os.path.exists(anyscale.project.ANYSCALE_AUTOSCALER_FILE):
            with open(anyscale.project.ANYSCALE_AUTOSCALER_FILE, "w") as f:
                f.write(anyscale.project.CLUSTER_YAML_TEMPLATE)
    project_definition = anyscale.project.ProjectDefinition(os.getcwd())
    project_definition.config["name"] = project_name
    return project_name, project_definition


@click.command(
    name="init", help="Create a new project or register an existing project."
)
@click.option("--name", help="Project name.", required=False)
@click.option(
    "--config",
    help="Path to autoscaler yaml. Created by default.",
    type=click.Path(exists=True),
    required=False,
)
@click.option(
    "--requirements",
    help="Path to requirements.txt. Created by default.",
    required=False,
)
@click.pass_context
# flake8: noqa: C901
def anyscale_init(
    ctx: Any, name: Optional[str], config: Optional[str], requirements: Optional[str],
) -> None:
    # Send an initial request to the server to make sure we are actually
    # registered. We only want to create the project if that is the case,
    # to avoid projects that are created but not registered.
    api_client = get_api_client()
    with format_api_exception(ApiException):
        api_client.get_user_info_api_v2_userinfo_get()

    project_name = ""
    project_id_path = anyscale.project.ANYSCALE_PROJECT_FILE

    if config:
        validate_cluster_configuration(config, api_instance=api_client)

    if os.path.exists(project_id_path):
        # Project id exists.
        try:
            project_definition = load_project_or_throw()
            project_id = project_definition.config["project_id"]
        except click.ClickException as e:
            raise e

        # Checking if the project is already registered.
        with format_api_exception(ApiException):
            resp = api_client.list_projects_api_v2_projects_get()
        for project in resp.results:
            if project.id == project_id:
                if not os.path.exists(anyscale.project.ANYSCALE_AUTOSCALER_FILE):
                    # Session yaml file doesn't exist.
                    project_name = get_project_directory_name(project.id)
                    url = get_endpoint(f"/projects/{project.id}")
                    if click.confirm(
                        "Session configuration missing in local project. Would "
                        "you like to replace your local copy of {project_name} "
                        "with the version in Anyscale ({url})?".format(
                            project_name=project_name, url=url
                        )
                    ):
                        clone_files(project_name, os.getcwd(), project.id)
                        print(f"Created project {project.id}. View at {url}")
                        return
                else:
                    raise click.ClickException(
                        "This project is already created at {url}.".format(
                            url=get_endpoint(f"/projects/{project.id}")
                        )
                    )
        # Project id exists locally but not registered in the db.
        if click.confirm(
            "The Anyscale project associated with this doesn't "
            "seem to exist anymore. Do you want to re-create it?",
            abort=True,
        ):
            os.remove(project_id_path)
            if os.path.exists(anyscale.project.ANYSCALE_AUTOSCALER_FILE):
                project_name, project_definition = create_new_proj_def(
                    name, project_definition.cluster_yaml(), api_instance=api_client
                )
            else:
                project_name, project_definition = create_new_proj_def(
                    name, config, api_instance=api_client
                )
    else:
        # Project id doesn't exist and not enough info to create project.
        project_name, project_definition = create_new_proj_def(
            name, config, api_instance=api_client
        )

    register_project(project_definition, api_instance=api_client)


def remote_snapshot(
    project_id: str,
    session_name: str,
    tags: List[str],
    project_definition: ProjectDefinition,
    description: Optional[str] = None,
) -> str:
    session = get_project_session(project_id, session_name)

    resp = send_json_request(
        "/api/v2/sessions/{session_id}/take_snapshot".format(session_id=session["id"]),
        {"tags": tags, "description": description if description else "",},
        method="POST",
    )
    if "id" not in resp["result"]:
        raise click.ClickException(
            "Snapshot creation of session {} failed!".format(session["name"])
        )
    snapshot_id: str = resp["result"]["id"]
    return snapshot_id


@snapshot_cli.command(name="create", help="Create a snapshot of the current project.")
@click.option("--description", help="A description of the snapshot", default=None)
@click.option(
    "--session-name",
    help="If specified, a snapshot of the remote session"
    "with that name will be taken.",
    default=None,
)
@click.option(
    "--yes", "-y", is_flag=True, default=False, help="Don't ask for confirmation."
)
@click.option(
    "--tag",
    type=str,
    help="Tag for this snapshot. Multiple tags can be specified by repeating this option.",
    multiple=True,
)
def snapshot_create(
    description: Optional[str], session_name: Optional[str], yes: bool, tag: List[str],
) -> None:
    project_definition = load_project_or_throw()
    project_id = get_project_id(project_definition.root)

    if session_name:
        # Create a remote snapshot.
        try:
            snapshot_id = remote_snapshot(
                project_id, session_name, tag, project_definition, description
            )
            print(
                "Snapshot {snapshot_id} of session {session_name} created!".format(
                    snapshot_id=snapshot_id, session_name=session_name
                )
            )
        except click.ClickException as e:
            raise e

    else:
        # Create a local snapshot.
        raise NotImplementedError("Local snapshotting is not supported anymore.")

    url = get_endpoint(f"/projects/{project_id}")
    print(f"Snapshot {snapshot_id} created. View at {url}")


@snapshot_cli.command(
    name="describe", help="Describe metadata and files of a snapshot."
)
@click.argument("name")
def snapshot_describe(name: str) -> None:
    try:
        description = describe_snapshot(name)
    except Exception as e:
        # Describing a snapshot can fail if the snapshot does not exist.
        raise click.ClickException(e)  # type: ignore

    print(description)


@session_cli.command(name="attach", help="Open a console for the given session.")
@click.option("--name", help="Name of the session to open a console for.", default=None)
@click.option("--tmux", help="Attach console to tmux.", is_flag=True)
@click.option("--screen", help="Attach console to screen.", is_flag=True)
def session_attach(name: Optional[str], tmux: bool, screen: bool) -> None:
    project_definition = load_project_or_throw()
    project_id = get_project_id(project_definition.root)

    session = get_project_session(project_id, name)
    ray.autoscaler._private.commands.attach_cluster(
        project_definition.cluster_yaml(),
        start=False,
        use_tmux=tmux,
        use_screen=screen,
        override_cluster_name=session["name"],
        new=False,
    )


@click.command(
    name="up",
    context_settings=dict(ignore_unknown_options=True,),
    help="Start or update a session based on the current project configuration.",
)
@click.argument("session-name", required=False)
@click.option(
    "--config", "config", help="Cluster to start session with.", default=None,
)
@click.option(
    "--no-restart",
    is_flag=True,
    default=False,
    help=(
        "Whether to skip restarting Ray services during the update. "
        "This avoids interrupting running jobs."
    ),
)
@click.option(
    "--restart-only",
    is_flag=True,
    default=False,
    help=(
        "Whether to skip running setup commands and only restart Ray. "
        "This cannot be used with 'no-restart'."
    ),
)
@click.option(
    "--min-workers",
    required=False,
    type=int,
    help="Override the configured min worker node count for the cluster.",
)
@click.option(
    "--max-workers",
    required=False,
    type=int,
    help="Override the configured max worker node count for the cluster.",
)
@click.option(
    "--disable-sync",
    is_flag=True,
    default=False,
    help=(
        "Disables syncing file mounts and project directory. This is "
        "useful when 'restart-only' is set and file syncing takes a long time."
    ),
)
@click.option("--cloud-id", required=False, help="Id of the cloud to use", default=None)
@click.option(
    "--cloud-name", required=False, help="Name of the cloud to use", default=None
)
@click.option(
    "--yes", "-y", is_flag=True, default=False, help="Don't ask for confirmation."
)
def anyscale_up(
    session_name: Optional[str],
    config: Optional[str],
    min_workers: Optional[int],
    max_workers: Optional[int],
    no_restart: bool,
    restart_only: bool,
    disable_sync: bool,
    cloud_id: Optional[str],
    cloud_name: Optional[str],
    yes: bool,
) -> None:
    """Create or update a Ray cluster."""

    project_definition = load_project_or_throw()
    project_id = get_project_id(project_definition.root)

    if not session_name:
        session_list = send_json_request(
            "/api/v2/sessions/", {"project_id": project_id, "active_only": False}
        )["results"]
        session_name = "session-{0}".format(len(session_list) + 1)

    config_attribute_provided = True
    if not config:
        config_attribute_provided = False
        config = project_definition.cluster_yaml()

    if not os.path.exists(config):
        if config_attribute_provided:
            raise ValueError("Config file {} not found".format(config))
        else:
            raise ValueError(
                "No config param provided and default config file session-default.yaml not found. Please provide a config file using the --config attribute."
            )
    with open(config) as f:
        cluster_config_filled = populate_session_args(f.read(), config)
        cluster_config = yaml.safe_load(cluster_config_filled)

    validate_cluster_configuration(config, cluster_config)

    if cloud_id:
        resp_get_cloud = send_json_request("/api/v2/clouds/{}".format(cloud_id), {})
        cloud = resp_get_cloud["result"]
    elif cloud_name:
        resp_get_cloud = send_json_request(
            "/api/v2/clouds/find_by_name", {"name": cloud_name}, method="POST"
        )
        cloud = resp_get_cloud["result"]
        cloud_id = cloud["id"]
    else:
        cloud = get_user_cloud()
        cloud_id = cloud["id"]

    assert cloud is not None, "Failed to get cloud."

    resp_out_up = send_json_request(
        "/api/v2/sessions/up",
        {
            "project_id": project_id,
            "name": session_name,
            "cluster_config": {"config": json.dumps(cluster_config)},
            "cloud_id": cloud_id,
        },
        method="POST",
    )

    session_id = resp_out_up["result"]["session_id"]

    # Getting the anyscale wheel
    wheel_resp = send_json_request_raw(
        f"/api/v2/sessions/{session_id}/anyscale_wheel", {},
    )
    wheel_path_raw = wheel_resp.headers["content-disposition"]
    assert "filename" in wheel_path_raw, "Error getting anyscale wheel"
    wheel_path = wheel_path_raw.split("filename=")[1].strip('"')
    os.makedirs(os.path.dirname(wheel_path), exist_ok=True)

    with open(wheel_path, "wb+") as f:  # type: ignore
        f.write(wheel_resp.content)  # type: ignore
        f.flush()

    prev_head_ip = send_json_request(
        "/api/v2/sessions/{}".format(resp_out_up["result"]["session_id"]), {}
    )["result"]["head_node_ip"]

    cluster_config = resp_out_up["result"]["cluster_config"]

    if not yes and not resp_out_up["result"]["is_same_cluster_config"]:
        create_cluster = click.confirm(
            f"The configuration stored for this session is different than that in {config}. "
            "Do you want to update the stored session configuration? The current session "
            "configuration can be found at {url}".format(
                url=get_endpoint(f"/projects/{project_id}")
            ),
        )
        if not create_cluster:
            send_json_request(
                "/api/v2/sessions/{session_id}/finish_up".format(
                    session_id=resp_out_up["result"]["session_id"]
                ),
                {"startup_log": None, "new_session": False, "head_node_ip": "",},
                "POST",
            )
            return

    if cluster_config["provider"].get("type") != "kubernetes":
        cluster_config = configure_for_session(
            session_id,
            project_definition.root,
            _DO_NOT_USE_RAY_UP_ONLY_cluster_config=cluster_config,
        )

    if disable_sync:
        cluster_config["file_mounts"] = {}

    anyscale.util.install_anyscale_hooks(cluster_config)

    with tempfile.NamedTemporaryFile(mode="w") as config_file:
        renamed_config = copy.deepcopy(cluster_config)
        renamed_config["cluster_name"] = resp_out_up["result"]["cluster_name"]
        json.dump(renamed_config, config_file)
        config_file.flush()
        try:
            # Use the bundled Autoscaler by directly calling the scripts file
            command = [
                sys.executable,
                autoscaler_scripts.__file__,
                "up",
                config_file.name,
                "--no-restart" if no_restart else "",
                "--restart-only" if restart_only else "",
                "--yes",
            ]
            command_lst = [c for c in command if c]
            if max_workers:
                command_lst.extend(["--max-workers", f"{max_workers}"])
            if min_workers:
                command_lst.extend(["--min-workers", f"{min_workers}"])
            proc = subprocess.Popen(
                command_lst,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                env=anyscale.ANYSCALE_ENV,
            )
            startup_log = []
            while proc.stdout:
                line = proc.stdout.readline().decode()
                if not line:
                    break
                print(line, end="")
                startup_log.append(line)
            startup_log_str = "".join(startup_log)
            proc.communicate()

            curr_head_ip = get_head_node_ip(renamed_config)

            # Rsync file mounts and project directory after cluster started
            if not disable_sync:
                rsync(
                    config_file.name,
                    source=None,
                    target=None,
                    override_cluster_name=None,
                    down=False,
                    all_nodes=True,
                )

            if curr_head_ip != prev_head_ip:
                print("Setting up Jupyter lab, Ray dashboard, and autosync ...")

            send_json_request(
                "/api/v2/sessions/{session_id}/finish_up".format(
                    session_id=resp_out_up["result"]["session_id"]
                ),
                {
                    "startup_log": startup_log_str,
                    "new_session": curr_head_ip != prev_head_ip,
                    "head_node_ip": curr_head_ip,
                },
                method="POST",
            )
            wait_for_session_start(project_id, session_name)
            url = get_endpoint(f"/projects/{project_id}")
            print(f"Session {session_name} started. View at {url}")
        except Exception as e:
            send_json_request(
                f"/api/v2/sessions/{resp_out_up['result']['session_id']}/stop",
                {"terminate": True, "workers_only": False, "keep_min_workers": False},
                method="POST",
            )
            raise click.ClickException("{}\nSession startup failed.".format(e))


@click.command(
    name="start",
    context_settings=dict(ignore_unknown_options=True,),
    help="Start a session based on the current project configuration.",
    hidden=True,
)
@click.option("--session-name", help="The name of the created session.", default=None)
# TODO(pcm): Change this to be
# anyscale session start --arg1=1 --arg2=2 command args
# instead of
# anyscale session start --session-args=--arg1=1,--arg2=2 command args
@click.option(
    "--session-args",
    help="Arguments that get substituted into the cluster config "
    "in the format --arg1=1,--arg2=2",
    default="",
)
@click.option(
    "--snapshot",
    help="If set, start the session from the given snapshot.",
    default=None,
)
@click.option(
    "--config",
    help="If set, use this cluster file rather than the default"
    " listed in project.yaml.",
    default=None,
)
@click.option(
    "--min-workers",
    help="Overwrite the minimum number of workers in the cluster config.",
    default=None,
)
@click.option(
    "--max-workers",
    help="Overwrite the maximum number of workers in the cluster config.",
    default=None,
)
@click.option(
    "--run", help="Command to run.", default=None,
)
@click.argument("args", nargs=-1, type=click.UNPROCESSED)
@click.option("--cloud-id", help="Id of the cloud to use", default=None)
@click.option("--cloud-name", help="Name of the cloud to use", default=None)
def anyscale_start(
    session_args: str,
    snapshot: Optional[str],
    session_name: Optional[str],
    config: Optional[str],
    min_workers: Optional[int],
    max_workers: Optional[int],
    run: Optional[str],
    args: List[str],
    cloud_id: Optional[str],
    cloud_name: Optional[str],
) -> None:
    command_name = run

    project_definition = load_project_or_throw()
    project_id = get_project_id(project_definition.root)

    if cloud_id and cloud_name:
        raise click.ClickException("Please provide either cloud id or cloud name.")
    elif cloud_name:
        resp_get_cloud = send_json_request(
            "/api/v2/clouds/find_by_name", {"name": cloud_name}, method="POST"
        )
        cloud = resp_get_cloud["result"]
        cloud_id = cloud["id"]

    if not session_name:
        session_list = send_json_request(
            "/api/v2/sessions/", {"project_id": project_id, "active_only": False}
        )["results"]
        session_name = "session-{0}".format(len(session_list) + 1)

    # Parse the session arguments.
    if config:
        project_definition.config["cluster"]["config"] = config

    session_params: Dict[str, str] = {}

    if command_name:
        command_name = " ".join([command_name] + list(args))
    session_runs = ray_scripts.get_session_runs(session_name, command_name, {})

    assert len(session_runs) == 1, "Running sessions with a wildcard is deprecated"
    session_run = session_runs[0]

    # TODO(ilr) Make snapshot_id optional, and have this only check if a snapshot is available
    snapshot_id = None
    if snapshot is not None:
        snapshot_id = get_snapshot_id(project_definition.root, snapshot)

    session_name = session_run["name"]
    resp = send_json_request(
        "/api/v2/sessions/",
        {"project_id": project_id, "name": session_name, "active_only": False},
    )
    if len(resp["results"]) == 0:
        resp = send_json_request(
            "/api/v2/sessions/create_new_session",
            {
                "project_id": project_id,
                "name": session_name,
                "snapshot_id": snapshot_id,
                "session_params": session_params,
                "command_name": command_name,
                "command_params": session_run["params"],
                "shell": True,
                "min_workers": min_workers,
                "max_workers": max_workers,
                "cloud_id": cloud_id,
            },
            method="POST",
        )
    elif len(resp["results"]) == 1:
        if session_params != {}:
            raise click.ClickException(
                "Session parameters are not supported when restarting a session"
            )
        send_json_request(
            "/api/v2/sessions/{session_id}/start".format(
                session_id=resp["results"][0]["id"]
            ),
            {"min_workers": min_workers, "max_workers": max_workers},
            method="POST",
        )
    else:
        raise click.ClickException(
            "Multiple sessions with name {} exist".format(session_name)
        )
    # Print success message
    url = get_endpoint(f"/projects/{project_id}")
    print(f"Session {session_name} starting. View progress at {url}")


@click.command(
    name="run",
    context_settings=dict(ignore_unknown_options=True,),
    help="Execute a command in a session.",
    hidden=True,
)
@click.argument("command_name", required=False)
@click.argument("args", nargs=-1, type=click.UNPROCESSED)
@click.option(
    "--session-name", help="Name of the session to run this command on", default=None
)
@click.option(
    "--stop", help="If set, stop session after command finishes running.", is_flag=True,
)
def anyscale_run(
    command_name: Optional[str],
    args: List[str],
    session_name: Optional[str],
    stop: bool,
) -> None:

    if not command_name:
        raise click.ClickException(
            "No shell command or registered command name was specified."
        )
    project_definition = load_project_or_throw()
    project_id = get_project_id(project_definition.root)
    session = get_project_session(project_id, session_name)

    command_name = " ".join([command_name] + list(args))

    send_json_request(
        "/api/v2/sessions/{session_id}/execute_shell_command".format(
            session_id=session["id"]
        ),
        {"shell_command": command_name, "stop": stop},
        method="POST",
    )


@session_cli.command(name="logs", help="Show logs for the current session.")
@click.option("--name", help="Name of the session to run this command on", default=None)
@click.option("--command-id", help="ID of the command to get logs for", default=None)
def session_logs(name: Optional[str], command_id: Optional[int]) -> None:
    project_definition = load_project_or_throw()
    project_id = get_project_id(project_definition.root)
    # If the command_id is not specified, determine it by getting the
    # last run command from the active session.
    if not command_id:
        session = get_project_session(project_id, name)
        resp = send_json_request(
            "/api/v2/session_commands/?session_id={}".format(session["id"]), {}
        )
        # Search for latest run command
        last_created_at = datetime.datetime.min
        last_created_at = last_created_at.replace(tzinfo=datetime.timezone.utc)
        for command in resp["results"]:
            created_at = deserialize_datetime(command["created_at"])
            if created_at > last_created_at:
                last_created_at = created_at
                command_id = command["id"]
        if not command_id:
            raise click.ClickException(
                "No comand was run yet on the latest active session {}".format(
                    session["name"]
                )
            )
    resp_out = send_json_request(
        "/api/v2/session_commands/{session_command_id}/execution_logs".format(
            session_command_id=command_id
        ),
        {"log_type": "out", "start_line": 0, "end_line": 1000000000},
    )
    resp_err = send_json_request(
        "/api/v2/session_commands/{session_command_id}/execution_logs".format(
            session_command_id=command_id
        ),
        {"log_type": "err", "start_line": 0, "end_line": 1000000000},
    )
    # TODO(pcm): We should have more options here in the future
    # (e.g. show only stdout or stderr, show only the tail, etc).
    print("stdout:")
    print(resp_out["result"]["lines"])
    print("stderr:")
    print(resp_err["result"]["lines"])


@session_cli.command(
    name="upload_command_logs", help="Upload logs for a command.", hidden=True
)
@click.option(
    "--command-id", help="ID of the command to upload logs for", type=str, default=None
)
def session_upload_command_logs(command_id: Optional[str]) -> None:
    resp = send_json_request(
        "/api/v2/session_commands/{session_command_id}/upload_logs".format(
            session_command_id=command_id
        ),
        {},
        method="POST",
    )
    assert resp["result"]["session_command_id"] == command_id

    allowed_sources = [
        execution_log_name(command_id) + ".out",
        execution_log_name(command_id) + ".err",
    ]

    for source, target in resp["result"]["locations"].items():
        if source in allowed_sources:
            copy_file(True, source, target, download=False)


@session_cli.command(
    name="finish_command", help="Finish executing a command.", hidden=True
)
@click.option(
    "--command-id", help="ID of the command to finish", type=str, required=True
)
@click.option(
    "--stop", help="Stop session after command finishes executing.", is_flag=True
)
def session_finish_command(command_id: str, stop: bool) -> None:
    with open(execution_log_name(command_id) + ".status") as f:
        status_code = int(f.read().strip())
    send_json_request(
        f"/api/v2/session_commands/{command_id}/finish",
        {"status_code": status_code, "stop": stop},
        method="POST",
    )


@click.command(
    name="cloudgateway",
    help="Run private clusters via anyscale cloud gateway.",
    hidden=True,
)
@click.option("--gateway-id", type=str, required=True)
def anyscale_cloudgateway(gateway_id: str) -> None:
    # Make sure only registered users can start the gateway.
    logger.info("Verifying user ...")
    try:
        send_json_request("/api/v2/userinfo/", {})
    except Exception:
        raise click.ClickException(
            "Invalid user. Did you set up the cli_token credentials?"
            + ' To setup your credentials, follow the instructions in the "credentials" tab'
            + " after logging in to your anyscale account."
        )
    anyscale_address = f"/api/v2/cloudgateway/{gateway_id}"
    cloudgateway_runner = CloudGatewayRunner(anyscale_address)
    logger.info(
        "Your gateway-id is: {}. Store it in the provider section in the".format(
            gateway_id
        )
        + " cluster yaml file of the remote cluster that interacts with this gateway."
        + ' E.g., config["provider"]["gateway_id"]={gateway_id}.'.format(
            gateway_id=gateway_id
        )
    )
    cloudgateway_runner.gateway_run_forever()


@click.command(
    name="autosync",
    short_help="Automatically synchronize a local project with a session.",
    help="""
This command launches the autosync service that will synchronize
the state of your local project with the Anyscale session that you specify.

If there is only a single session running, this command without arguments will
default to that session.""",
)
@click.argument("session-name", type=str, required=False, default=None)
@click.option("--verbose", help="Show output from autosync.", is_flag=True)
@click.option(
    "--sync-git", help="Whether to sync .git files.", is_flag=True, default=False,
)
def anyscale_autosync(
    session_name: Optional[str], verbose: bool, sync_git: bool
) -> None:
    project_definition = load_project_or_throw()
    project_id = get_project_id(project_definition.root)
    print(f"Active project: {project_definition.root}\n")

    session = get_project_session(project_id, session_name)

    wait_for_session_start(project_id, session["name"])

    # Get project directory name:
    directory_name = get_project_directory_name(project_id)

    cluster_config = get_cluster_config(session_name)

    head_ip = send_json_request(
        "/api/v2/sessions/{}/head_ip".format(session["id"]), {}
    )["result"]["head_ip"]
    ssh_user = cluster_config["auth"]["ssh_user"]
    ssh_private_key_path = cluster_config["auth"]["ssh_private_key"]

    source = project_definition.root
    target = get_working_dir(cluster_config, project_id)
    if bool(get_container_name(cluster_config)):
        target = f"{DOCKER_MOUNT_PREFIX}/{target}"
        # Legacy mount check
        old_mounts = [
            x
            for x in cluster_config["docker"].get("run_options", [])
            if f"$HOME/{directory_name}" in x
        ]
        if len(old_mounts) == 1:
            target = f"~/{directory_name}"

    print("Autosync with session {} is starting up...".format(session["name"]))
    with managed_autosync_session(session["id"]):
        ssh_command = [
            "ssh",
            "-o",
            "StrictHostKeyChecking=no",
            "-o",
            "UserKnownHostsFile={}".format(os.devnull),
            "-o",
            "LogLevel=ERROR",
            "-i",
            ssh_private_key_path,
        ]
        # Performing initial full synchronization with rsync.
        command = get_rsync_command(
            ssh_command, source, ssh_user, head_ip, target, sync_git,
        )
        first_sync = subprocess.run(command, shell=True)

        if first_sync.returncode != 0:
            raise click.ClickException(
                f"First sync failed with error code: {first_sync.returncode}"
            )

        current_dir = os.path.dirname(os.path.realpath(__file__))
        if sys.platform.startswith("linux"):
            env: Dict[str, str] = {}
            fswatch_executable = os.path.join(current_dir, "fswatch-linux")
            fswatch_command = [
                fswatch_executable,
                source,
                "--batch-marker",
                "--monitor=poll_monitor",
                "-r",
            ]
            if not sync_git:
                fswatch_command += ["-e", ".*/\.git"]
        elif sys.platform.startswith("darwin"):
            env = {"DYLD_LIBRARY_PATH": current_dir}
            fswatch_executable = os.path.join(current_dir, "fswatch-darwin")
            fswatch_command = [
                fswatch_executable,
                source,
                "--batch-marker",
            ]
            if not sync_git:
                fswatch_command += ["-e", ".*/\.git"]
        else:
            raise NotImplementedError(
                "Autosync not supported on platform {}".format(sys.platform)
            )

        # Perform synchronization whenever there is a change. We batch together
        # multiple updates and then call rsync on them.
        with subprocess.Popen(
            fswatch_command, stdout=subprocess.PIPE, env=env,
        ) as proc:
            while True:
                files = []
                while True and proc.stdout:
                    path = proc.stdout.readline().strip().decode()
                    if path == "NoOp":
                        break
                    else:
                        relpath = os.path.relpath(path, source)
                        files.append(relpath)
                if files:
                    # Filter out gitignore files
                    try:
                        ignored_files = subprocess.check_output(
                            ["git", "check-ignore", *files]
                        )
                        files_to_ignore = ignored_files.decode().splitlines()
                        for file in files_to_ignore:
                            files.remove(file)
                    except subprocess.CalledProcessError as e:
                        if e.returncode == 1:
                            # Nothing is being ignored, this is fine
                            pass
                        else:
                            raise e

                    with tempfile.NamedTemporaryFile(mode="w") as modified_files:
                        for f in files:
                            # Avoid rsyncing temporary files that may disappear between
                            # now and when rsync builds a file list.
                            # This matches files ending with: .swp, ~, .tmp or 4913 (neovim)
                            if re.match("(.*(.sw[a-e,g-z]|~|.tmp)$|^4913$)", f):
                                continue
                            modified_files.write(f + "\n")
                        modified_files.flush()
                        command = get_rsync_command(
                            ssh_command,
                            source,
                            ssh_user,
                            head_ip,
                            target,
                            sync_git,
                            modified_files=modified_files,
                        )
                        logger.info("Calling rsync due to detected file update.")
                        logger.debug("Command: {command}".format(command=command))
                        temp_sync = subprocess.run(command, shell=True)
                        if temp_sync.returncode != 0:
                            logger.error(
                                f"Secondary sync failed with error code: {temp_sync.returncode}, autosync will continue running."
                            )


@session_cli.command(name="auth_start", help="Start the auth proxy", hidden=True)
def auth_start() -> None:
    from aiohttp import web

    web.run_app(auth_proxy_app)


def _canonicalize_remote_location(
    cluster_config: Dict[str, Any], remote_location: Optional[str], project_id: str
) -> Optional[str]:
    # Include the /root path to ensure that absolute paths also work
    # This is because of an implementation detail in OSS Ray's rsync
    if bool(get_container_name(cluster_config)) and bool(remote_location):
        remote_location = str(remote_location)
        working_dir = get_working_dir(cluster_config, project_id)

        # TODO(ilr) upstream this to OSS Ray
        # TODO(ilr) move away from hardcoded /root
        if working_dir.startswith("~/") and remote_location.startswith("/root/"):
            return remote_location.replace("/root/", "~/", 1)

        if working_dir.startswith("/root/") and remote_location.startswith("~/"):
            return remote_location.replace("~/", "/root/", 1)

    return remote_location


@click.command(name="pull", help="Pull session")
@click.argument(
    "session-name", type=str, required=False, default=None, envvar="SESSION_NAME"
)
@click.option(
    "--source",
    "-s",
    type=str,
    required=False,
    default=None,
    help="Source location to transfer files located on head node of cluster "
    "from. If source and target are specified, only those files/directories "
    "will be updated.",
)
@click.option(
    "--target",
    "-t",
    type=str,
    required=False,
    default=None,
    help="Local target location to transfer files to. If source and target "
    "are specified, only those files/directories will be updated.",
)
@click.option(
    "--config",
    type=str,
    required=False,
    default=None,
    help="Pulls cluster configuration from session this location.",
)
@click.confirmation_option(
    prompt="Pulling a session will override the local project directory. Do you want to continue?"
)
def anyscale_pull_session(
    session_name: str,
    source: Optional[str],
    target: Optional[str],
    config: Optional[str],
) -> None:
    project_definition = load_project_or_throw()

    try:
        print("Collecting files from remote.")
        project_id = get_project_id(project_definition.root)
        directory_name = get_project_directory_name(project_id)
        source_directory = "~/{}/".format(directory_name)

        cluster_config = get_cluster_config(session_name)
        source = _canonicalize_remote_location(cluster_config, source, project_id)
        with tempfile.NamedTemporaryFile(mode="w") as config_file:
            json.dump(cluster_config, config_file)
            config_file.flush()

            if source and target:
                rsync(
                    config_file.name,
                    source=source,
                    target=target,
                    override_cluster_name=None,
                    down=True,
                )
            elif source or target:
                raise click.ClickException(
                    "Source and target are not both specified. Please either specify both or neither."
                )
            else:
                rsync(
                    config_file.name,
                    source=source_directory,
                    target=project_definition.root,
                    override_cluster_name=None,
                    down=True,
                )

        if config:
            session = get_project_session(project_id, session_name)
            resp = send_json_request(
                "/api/v2/sessions/{session_id}/cluster_config".format(
                    session_id=session["id"]
                ),
                {},
                "GET",
            )
            cluster_config = yaml.safe_load(resp["result"]["config_with_defaults"])
            with open(config, "w") as f:
                yaml.dump(cluster_config, f, default_flow_style=False)

        print("Pull completed.")

    except Exception as e:
        raise click.ClickException(e)  # type: ignore


@click.command(name="push", help="Push current project to session.")
@click.argument(
    "session-name", type=str, required=False, default=None, envvar="SESSION_NAME"
)
@click.option(
    "--source",
    "-s",
    type=str,
    required=False,
    default=None,
    help="Source location to transfer files located on head node of cluster "
    "from. If source and target are specified, only those files/directories "
    "will be updated.",
)
@click.option(
    "--target",
    "-t",
    type=str,
    required=False,
    default=None,
    help="Local target location to transfer files to. If source and target "
    "are specified, only those files/directories will be updated.",
)
@click.option(
    "--config",
    type=str,
    required=False,
    default=None,
    help="Updates session with this configuration file.",
)
@click.option(
    "--all-nodes",
    "-A",
    is_flag=True,
    required=False,
    help="Choose to update to all nodes (workers and head) if source and target are specified.",
)
@click.pass_context
def anyscale_push_session(
    ctx: Any,
    session_name: str,
    source: Optional[str],
    target: Optional[str],
    config: Optional[str],
    all_nodes: bool,
) -> None:
    project_definition = load_project_or_throw()
    project_id = get_project_id(project_definition.root)
    session = get_project_session(project_id, session_name)
    session_name = session["name"]

    cluster_config = get_cluster_config(session_name)
    target = _canonicalize_remote_location(cluster_config, target, project_id)
    with tempfile.NamedTemporaryFile(mode="w") as config_file:
        json.dump(cluster_config, config_file)
        config_file.flush()

        if source and target:
            rsync(
                config_file.name,
                source=source,
                target=target,
                override_cluster_name=None,
                down=False,
                all_nodes=all_nodes,
            )
        elif source or target:
            raise click.ClickException(
                "Source and target are not both specified. Please either specify both or neither."
            )
        else:
            rsync(
                config_file.name,
                source=None,
                target=None,
                override_cluster_name=None,
                down=False,
                all_nodes=True,
            )

    if config:
        validate_cluster_configuration(config)
        print("Updating session with {}".format(config))
        ctx.invoke(
            anyscale_up,
            session_name=session_name,
            no_restart=False,
            restart_only=False,
            disable_sync=True,
            yes=True,
            cloud_id=session["cloud_id"],
        )

    url = get_endpoint(f"/projects/{project_id}")
    print(f"Pushed to session {session_name}. View at {url}")


@click.command(
    name="clone",
    short_help="Clone a project that exists on anyscale, to your local machine.",
    help="""Clone a project that exists on anyscale, to your local machine.
This command will create a new folder on your local machine inside of
the current working directory and download the most recent snapshot.

This is frequently used with anyscale push or anyscale pull to download, make
changes, then upload those changes to a currently running session.""",
)
@click.argument("project-name", required=True)
def anyscale_clone(project_name: str) -> None:
    resp = send_json_request("/api/v2/projects/", {})
    project_names = [p["name"] for p in resp["results"]]
    project_ids = [p["id"] for p in resp["results"]]

    if project_name not in project_names:
        raise click.ClickException(
            "No project with name {} found.".format(project_name)
        )
    project_id = project_ids[project_names.index(project_name)]

    os.makedirs(project_name)
    clone_files(project_name, project_name, project_id)


def clone_files(project_name: str, directory: str, project_id: str) -> None:
    with open("{}/{}".format(directory, ANYSCALE_PROJECT_FILE), "w") as f:
        f.write("{}".format("project_id: {}".format(project_id)))

    sessions_resp = send_json_request("/api/v2/sessions/", {"project_id": project_id})
    sessions = sessions_resp["results"]

    if len(sessions) > 0:
        lastest_session = sessions[0]

        cluster_config_resp = send_json_request(
            "/api/v2/sessions/{}/cluster_config".format(lastest_session["id"]), {}
        )
        cluster_config = cluster_config_resp["result"]["config"]
    else:
        cluster_config_resp = send_json_request(
            "/api/v2/projects/{}/latest_cluster_config".format(project_id), {}
        )
        cluster_config = cluster_config_resp["result"]["config"]

    cluster_config_dict = json.loads(cluster_config)

    with open("{}/{}".format(directory, ANYSCALE_AUTOSCALER_FILE), "w") as f:
        yaml.dump(cluster_config_dict, f)


@click.command(name="ssh", help="SSH into head node of cluster.")
@click.argument(
    "session-name", type=str, required=False, default=None, envvar="SESSION_NAME"
)
@click.option("-o", "--ssh-option", multiple=True)
def anyscale_ssh(session_name: str, ssh_option: Tuple[str]) -> None:
    project_definition = load_project_or_throw()
    project_id = get_project_id(project_definition.root)
    session = get_project_session(project_id, session_name)

    cluster_config = get_cluster_config(session_name)

    head_ip = send_json_request(
        "/api/v2/sessions/{}/head_ip".format(session["id"]), {}
    )["result"]["head_ip"]
    ssh_user = cluster_config["auth"]["ssh_user"]
    key_path = cluster_config["auth"]["ssh_private_key"]
    container_name = get_container_name(cluster_config)

    command = (
        ["ssh"]
        + list(ssh_option)
        + ["-tt", "-i", key_path]
        + ["{}@{}".format(ssh_user, head_ip)]
        + (
            [f"docker exec -it {container_name} sh -c 'which bash && bash || sh'"]
            if container_name
            else []
        )
    )

    subprocess.run(command)


@cli.command(
    name="rsync-down", help="Download specific files from cluster.", hidden=True
)
@click.argument("session-name", required=False, type=str)
@click.argument("source", required=False, type=str)
@click.argument("target", required=False, type=str)
@click.option(
    "--cluster-name",
    "-n",
    required=False,
    type=str,
    help="Override the configured cluster name.",
)
def anyscale_rsync_down(
    session_name: Optional[str],
    source: Optional[str],
    target: Optional[str],
    cluster_name: Optional[str],
) -> None:
    project_definition = load_project_or_throw()
    project_id = get_project_id(project_definition.root)

    session = get_project_session(project_id, session_name)

    cluster_config = get_cluster_config(session["name"])
    with tempfile.NamedTemporaryFile(mode="w") as config_file:
        cluster_config["cluster_name"] = cluster_name
        json.dump(cluster_config, config_file)
        config_file.flush()
        rsync(
            config_file.name,
            source=source,
            target=target,
            override_cluster_name=None,
            down=True,
        )


@cli.command(name="rsync-up", help="Upload specific files to cluster.", hidden=True)
@click.argument("session-name", required=False, type=str)
@click.argument("source", required=False, type=str)
@click.argument("target", required=False, type=str)
@click.option(
    "--cluster-name",
    "-n",
    required=False,
    type=str,
    help="Override the configured cluster name.",
)
@click.option(
    "--all-nodes",
    "-A",
    is_flag=True,
    required=False,
    help="Upload to all nodes (workers and head).",
)
def anyscale_rsync_up(
    session_name: Optional[str],
    source: Optional[str],
    target: Optional[str],
    cluster_name: Optional[str],
    all_nodes: bool,
) -> None:
    project_definition = load_project_or_throw()
    project_id = get_project_id(project_definition.root)

    session = get_project_session(project_id, session_name)

    cluster_config = get_cluster_config(session["name"])
    with tempfile.NamedTemporaryFile(mode="w") as config_file:
        json.dump(cluster_config, config_file)
        config_file.flush()
        rsync(
            config_file.name,
            source,
            target,
            cluster_name,
            down=False,
            all_nodes=all_nodes,
        )


cli.add_command(project_cli)
cli.add_command(session_cli)
cli.add_command(snapshot_cli)
cli.add_command(cloud_cli)
cli.add_command(version_cli)
cli.add_command(list_cli)


@click.group("ray", help="Open source Ray commands.")
@click.pass_context
def ray_cli(ctx: Any) -> None:
    subcommand = autoscaler_scripts.cli.commands[ctx.invoked_subcommand]
    # Replace the cluster_config_file argument with a session_name argument.
    if subcommand.params[0].name == "cluster_config_file":
        subcommand.params[0] = click.Argument(["session_name"])

    original_autoscaler_callback = copy.deepcopy(subcommand.callback)

    if "--help" not in sys.argv and ctx.invoked_subcommand in ["up", "down"]:
        args = sys.argv[3:]

        if ctx.invoked_subcommand == "up":
            old_command = "anyscale ray up {}".format(" ".join(args))
            new_command = "anyscale start --config {}".format(" ".join(args))
        else:
            old_command = "anyscale ray down {}".format(" ".join(args))
            new_command = "anyscale down SESSION_NAME {}".format(" ".join(args[1:]))

        print(
            "\033[91m\nYou called\n  {}\nInstead please call\n  {}\033[00m".format(
                old_command, new_command
            )
        )

        sys.exit()

    def autoscaler_callback(*args: Any, **kwargs: Any) -> None:
        try:
            if "session_name" in kwargs:
                # Get the cluster config. Use kwargs["session_name"] as the session name.
                cluster_config = get_cluster_config(kwargs["session_name"])
                del kwargs["session_name"]
                with tempfile.NamedTemporaryFile(mode="w") as config_file:
                    json.dump(cluster_config, config_file)
                    config_file.flush()
                    kwargs["cluster_config_file"] = config_file.name
                    original_autoscaler_callback(*args, **kwargs)
            else:
                original_autoscaler_callback(*args, **kwargs)
        except Exception as e:
            raise click.ClickException(e)  # type: ignore

    subcommand.callback = autoscaler_callback


def install_autoscaler_shims(ray_cli: Any) -> None:
    for name, command in autoscaler_scripts.cli.commands.items():
        if isinstance(command, click.core.Group):
            continue
        ray_cli.add_command(command, name=name)


install_autoscaler_shims(ray_cli)
cli.add_command(ray_cli)

cli.add_command(anyscale_init)
cli.add_command(anyscale_run)
cli.add_command(anyscale_start)
cli.add_command(anyscale_up)
cli.add_command(anyscale_stop)
cli.add_command(anyscale_cloudgateway)
cli.add_command(anyscale_autosync)
cli.add_command(anyscale_clone)
cli.add_command(anyscale_ssh)
cli.add_command(anyscale_rsync_down)
cli.add_command(anyscale_rsync_up)
cli.add_command(anyscale_exec)
cli.add_command(anyscale_push_session)
cli.add_command(anyscale_pull_session)
cli.add_command(anyscale_help)

ALIASES = {"h": anyscale_help}


def main() -> Any:
    return cli()


if __name__ == "__main__":
    main()

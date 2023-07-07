"""This module provides the BeS-dev-kit CLI."""
# src/cli.py
import os
import ssl
import json
import sys
from sys import platform
from typing import Optional
from typing import List
from rich import print
import typer
from bes_dev_kit import __app_name__, __version__
from bes_dev_kit.src.create_ossp_master import OSSPMaster
from bes_dev_kit.src.create_version_data import Version
from bes_dev_kit.src.generate_report import Report
from bes_dev_kit.src.validate_version_file import VersionFileValidate
from bes_dev_kit.src.risk_assessment import Generate_report
from bes_dev_kit.src.validate_report_file import ReportFileValidate

ssl._create_default_https_context = ssl._create_stdlib_context

def write_env_vars_file():
    """Creates an env var file
    """
    user_home = os.path.expanduser('~')
    vars_dir_path = f"{user_home}/.bes-dev-kit"
    vars_file_path = f"{vars_dir_path}/bes-dev-kit.json"
    env_vars = {
        "GITHUB_ORG": "Be-Secure",
        "OSSPOI_DIR": "",
        "ASSESSMENT_DIR": "",
        "GITHUB_AUTH_TOKEN": ""
    }
    if os.path.exists(vars_file_path) and os.stat(vars_file_path).st_size > 0:
        return
    os.makedirs(vars_dir_path, exist_ok=True)
    print("[bold red]Alert! [green]Creating environment variables file")
    with open(vars_file_path, 'w', encoding="utf-8") as file_pointer:
        file_pointer.write(json.dumps(env_vars, indent=4))


def prompt_user(key, value):
    """Prompts user if any env var is empty

    Args:
        key (_type_): env var key
        value (_type_): env var value

    Returns:
        _type_: value
    """
    while True:
        value = input(f"Enter the value for {key}:")
        if key != "GITHUB_AUTH_TOKEN" and not os.path.exists(value):
            print("[bold red]Alert! [green]Path " +
                  f"[yellow]{value} [green]does not exist")
        else:
            break
    return value

def check_if_value_empty():
    """Checks if any env var is empty. Calls function prompt_user if empty
    """
    user_home = os.path.expanduser('~')
    vars_dir_path = f"{user_home}/.bes-dev-kit"
    vars_file_path = f"{vars_dir_path}/bes-dev-kit.json"
    with open(vars_file_path, 'r+', encoding="utf-8") as file_pointer:
        env_vars = json.load(file_pointer)
        for key, value in env_vars.items():
            if value == "":
                new_value = prompt_user(key, value)
                env_vars[key] = new_value
        file_pointer.seek(0)
        file_pointer.write(json.dumps(env_vars, indent=4))

def set_env_vars():
    """Adds the env env_vars to os.environment
    """
    user_home = os.path.expanduser('~')
    vars_dir_path = f"{user_home}/.bes-dev-kit"
    vars_file_path = f"{vars_dir_path}/bes-dev-kit.json"
    with open(vars_file_path, 'r', encoding="utf-8") as file_pointer:
        env_vars = json.load(file_pointer)
    for key, value in env_vars.items():
        os.environ[key] = str(value)


app = typer.Typer()

def _version_callback(value: bool) -> None:
    if value:
        typer.echo(f"{__app_name__} v{__version__}")
        raise typer.Exit()


@app.command("generate-metadata")
def ossp(
    issue_id: int = typer.Option(None, prompt="Enter OSSP id", help="OSSP id"),
    name: str = typer.Option(None, prompt="Enter OSSP name", help="OSSP name"),
    overwrite: bool = typer.Option(False, help="Overwrite the existing entries")
    ):
    """ Update OSSP-master.json file and add/update version file to osspoi datastore """
    if platform != "linux":
        print("[bold red]BeS-dev-kit is compatible"
              " only with Linux operating systems")
        raise typer.Exit()
    write_env_vars_file()
    check_if_value_empty()
    set_env_vars()
    ossp_data = OSSPMaster(issue_id, name)
    ossp_data.generate_ossp_master(overwrite)
    version_data = Version(issue_id, name)
    version_data.generate_version_data(overwrite)


@app.command("generate-report")
def report(
    reports: List[str] = typer.Argument(None),
    issue_id: int = typer.Option(None, prompt="Enter OSSP id", help="OSSP id"),
    name: str = typer.Option(None, prompt="Enter OSSP name", help="OSSP name"),
    version: str = typer.Option(None, prompt="Enter version", help="Version of OSSP"),
    update_version_file: bool = typer.Option(True, help="Update scores to version file"),
    ):
    """ Following reports can be generated - scorecard, criticality_score, codeql, sbom"""
    if platform != "linux":
        print("[bold red]BeS-dev-kit is compatible"
              " only with Linux operating systems")
        raise typer.Exit()
    write_env_vars_file()
    check_if_value_empty()
    set_env_vars()
    assessment_reports = [
                'scorecard',
                'criticality_score',
                'codeql',
                'sbom']
    if reports:
        if len(reports) > 4:
            print("[bold red]Alert! [green]Too many arguments")
            raise typer.Exit()
        # check if given parameters are valid
        for i in reports:
            if i.lower() not in assessment_reports:
                print('[red bold]Alart! [green]'
                    'Invalid input'
                    f' [yellow]{i}')
                sys.exit(1)
        assessment_reports = reports
    for i in assessment_reports:
        print('\n')
        print("[bold yellow]Generating " + i.lower() + ' report....')
        obj = Report(issue_id, name, version, i.lower())
        obj.main()
        if update_version_file and (i.lower() == "scorecard" or i.lower() == "criticality_score"):
            obj.update_version_data()
    raise typer.Exit()


@app.command("validate-version-file")
def version_data_naming_convention_validation(
    issue_id: int = typer.Option(
                        None,
                        prompt="Enter OSSP id",
                        help="OSSP id"
                    ),
    name: str = typer.Option(
                        None,
                        prompt="Enter OSSP name",
                        help="OSSP name"
                    ),
    namespace: str = typer.Option(
                        None,
                        prompt="Enter GitHub username",
                        help="GitHub Username"
                    ),
    branch: str = typer.Option(
                        None,
                        prompt="Enter branch",
                        help="besecure-osspoi-datastore branch"
                    ),
    ):
    """ Check version details file naming convention """
    if platform != "linux":
        print("[bold red]BeS-dev-kit is compatible"
              " only with Linux operating systems")
        raise typer.Exit()
    version_data = VersionFileValidate(issue_id, name, namespace, branch)
    version_data.verify_versiondetails_name()


@app.command("validate-report-file")
def report_naming_convention_validation(
    reports: List[str] = typer.Argument(None),
    get_all: bool = typer.Option(False, help="Get all 3 reports"),
    issue_id: int = typer.Option(
                        None,
                        prompt="Enter OSSP id",
                        help="OSSP id"
                    ),
    name: str = typer.Option(
                        None,
                        prompt="Enter OSSP name",
                        help="OSSP name"
                    ),
    namespace: str = typer.Option(
                        None,
                        prompt="Enter GitHub username",
                        help="GitHub Username"
                    ),
    branch: str = typer.Option(
                        None,
                        prompt="Enter branch",
                        help="besecure-osspoi-datastore branch"
                    )
):
    """ Check report file naming convention """
    if platform != "linux":
        print("[bold red]BeS-dev-kit is compatible"
              " only with Linux operating systems")
        raise typer.Exit()
    report_list = ["scorecard",
                   "criticality_score",
                   "codeql",
                   'fossology',
                   'sonarqube',
                   'sbom']
    if reports:
        if len(reports) > 6:
            print("[bold red]Alert! [green]Too many arguments")
            raise typer.Exit()
        # check if given parameters are valid
        for i in reports:
            if i.lower() not in report_list:
                print('[red bold]Alart! [green]'
                    'Invalid input:'
                    f' [yellow]{i}')
                sys.exit(1)
        report_list = reports
    obj = ReportFileValidate(
            issue_id,
            name.strip(),
            namespace.strip(),
            branch.strip())
    obj.validateIssue()
    for report_name in report_list:
        report_name = report_name.lower().strip()
        obj.validate_report_file(report_name)


@app.command('risk-summary')
def download_consolidate_assessment_report(
    OSSP_name: str = typer.Option(
                    None,
                    prompt="Enter OSSP Name",
                    help="OSSP Name"
                ),
    version: str = typer.Option(
                    None,
                    prompt="Enter OSSP Version",
                    help="OSSP Version"
                ),
    ):
    """Download consolidated assessment report in pdf format"""
    if platform != "linux":
        print("[bold red]BeS-dev-kit is compatible"
              " only with Linux operating systems")
        raise typer.Exit()
    report = Generate_report()
    report.download_pdf(OSSP_name, version)

@app.callback()
def main(
    version: Optional[bool] = typer.Option(
        None,
        "--version",
        "-v",
        help="Show the application's version and exit.",
        callback=_version_callback,
        is_eager=True,
    )
):
    """Callback function for version
    """
    return

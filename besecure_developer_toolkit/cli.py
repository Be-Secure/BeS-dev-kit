"""This module provides the Be-Secure Developer Toolkit CLI."""
# src/cli.py
import sys, os, json
from typing import Optional
from typing import List
from rich import print
import typer
from besecure_developer_toolkit import __app_name__, __version__
from besecure_developer_toolkit.src.CreateOsspMaster import OSSPMaster
from besecure_developer_toolkit.src.CreateVersionData import Version
from besecure_developer_toolkit.src.GenerateReport import Report

def set_env_vars():
    user_home = os.path.expanduser('~')
    with open(user_home+'/bes_dev_kit.json', 'r') as f:
        vars = json.load(f)
    for key, value in vars.items():
        os.environ[key] = str(value)

set_env_vars()

app = typer.Typer()

generate_app = typer.Typer()

app.add_typer(generate_app, name="generate")

def _version_callback(value: bool) -> None:
    if value:
        typer.echo(f"{__app_name__} v{__version__}")
        raise typer.Exit()



@generate_app.command("metadata")
def ossp(overwrite: bool = typer.Option(False, help="Overwrite the existing entries inside OSSP-master.json and version file")):
    """ Update OSSP-master.json file and add/update version file to osspoi datastore """
    try:
        id = int(input("Enter OSSP id:"))
    except ValueError:
        sys.exit("Input should be of type int")
    name = str(input("Enter OSSP name:"))
    ossp_data = OSSPMaster(id, name)
    ossp_data.GenerateOsspMaster(overwrite)
    version_data = Version(id, name)
    version_data.generate_version_data(overwrite)

@generate_app.command("report")
def report(reports: List[str], update_version_file: bool = typer.Option(True, help="Update version file with scorecard/criticality score")):
    """ Following reports can be generated - scorecard, criticality_score, codeql"""
    if len(reports) > 3:
        print("[bold red]Alert! [green]Too many arguments")
        raise typer.Exit()
    else:
        try:
            id = int(input("Enter OSSP id:"))
        except ValueError:
            print("[bold red]Alert! [green]Expected type int")
            raise typer.Exit()
            
        name = str(input("Enter OSSP name:"))
        version = str(input("Enter version of "+ name +":"))
        for i in reports:
            if i == "scorecard":
               scorecard_obj = Report(id, name, version, i)
               scorecard_obj.main()
               if update_version_file:
                   scorecard_obj.update_version_data()
            elif i == "criticality_score":
                criticality_obj = Report(id, name, version, i)
                criticality_obj.main()
                if update_version_file:   
                    criticality_obj.update_version_data()
            elif i == "codeql":
                codeql_obj = Report(id, name, version, i)
                codeql_obj.main()
    

    
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

    return
import os
import click
from src.generate_report import generateReport

CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])

@click.group(context_settings=CONTEXT_SETTINGS)
def cli():
    pass

@cli.command("osspoi")
def generate_report():
    """Provide path to besecure-osspoi-datastore to generate report for OSSP-Master.json and version_details eg: assessment_report osspoi 'path'"""
    try:
        besecureOsspoi = os.environ["BESECURE_OSSPOI_DATASTORE_PATH"]
        besecureAssessment = os.environ["BESECURE_ASSESSMENT_DATASTORE_PATH"]
        ghToken = os.environ["GITHUB_AUTH_TOKEN"]
    except Exception as e:
        raise Exception(f'Please set environment variable for {e}, eg: \n for windows: set {e}=<your input> \n for Linux, mac export {e}=<your input>')
    id = input("Provide id of project: ")
    name = input("Provide name of project: ")
    
    try:

        report = generateReport(name, id)
        report.osspoiMasterReport(besecureOsspoi)
        report.osspoiVersionReport(besecureOsspoi)
        report.codeQlReport(ghToken, besecureAssessment)
    except Exception as e:
        click.echo(f"Fails to generate report for besecure-osspoi-datastore error: {e}")
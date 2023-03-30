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
    id = input("Provide id of project: ")
    name = input("Provide name of project: ")
    try:
        report = generateReport(name, id)
        report.osspoiMasterReport()
        click.echo("jklsjkljdlfjdkjkljdfkljdf")
        report.osspoiVersionReport()

        # besecureSsspoi = os.environ["BESECURE_OSSPOI_DATASTORE_PATH"]
        # besecureAssessment = os.environ["BESECURE_ASSESSMENT_DATASTORE_PATH"]
        # ghToken = os.environ["GITHUB_AUTH_TOKEN"]
    except Exception as e:
        click.echo(f"Fails to generate report for besecure-osspoi-datastore error: {e}")
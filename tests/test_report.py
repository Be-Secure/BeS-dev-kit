from typer.testing import CliRunner
import os, json

from besecure_developer_toolkit.cli import app

runner = CliRunner()

def test_scorecard():
    id = "136"
    name = "fastjson"
    version = "1.2.24"
    assessment_dir = os.environ['ASSESSMENT_DIR']
    result = runner.invoke(app, ["generate", "report", "scorecard"], input=id+"\n"+name+"\n"+version+"\n")
    assert result.exit_code == 0
    scorecard_exist = os.path.exists(f'{assessment_dir}/{name}/{version}/scorecard/{name}-{version}-scorecard-report.json')
    assert scorecard_exist == True
    size = os.path.getsize(f'{assessment_dir}/{name}/{version}/scorecard/{name}-{version}-scorecard-report.json')
    assert size > 0

def test_criticality():
    id = "136"
    name = "fastjson"
    version = "1.2.24"
    assessment_dir = os.environ['ASSESSMENT_DIR']
    result = runner.invoke(app, ["generate", "report", "criticality_score"], input=id+"\n"+name+"\n"+version+"\n")
    assert result.exit_code == 0
    criticality_exist = os.path.exists(f'{assessment_dir}/{name}/{version}/criticality_score/{name}-{version}-criticality_score-report.json')
    assert criticality_exist == True
    size = os.path.getsize(f'{assessment_dir}/{name}/{version}/scorecard/{name}-{version}-scorecard-report.json')
    assert size > 0

def test_codeql():
    id = "136"
    name = "fastjson"
    version = "1.2.24"
    assessment_dir = os.environ['ASSESSMENT_DIR']
    result = runner.invoke(app, ["generate", "report", "codeql"], input=id+"\n"+name+"\n"+version+"\n")
    assert result.exit_code == 0
    codeql_exist = os.path.exists(f'{assessment_dir}/{name}/{version}/sast/{name}-{version}-codeql-report.json')
    assert codeql_exist == True
    size = os.path.getsize(f'{assessment_dir}/{name}/{version}/scorecard/{name}-{version}-scorecard-report.json')
    assert size > 0
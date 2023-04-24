"""Test cases for version details file naming convention"""
from typer.testing import CliRunner
from besecure_developer_toolkit.cli import app

runner = CliRunner()


def test_vdnc():
    """test with valid data"""
    issue_id = 136
    name = "fastjson"
    namespace = "Be-Secure"
    branch = "main"

    result = runner.invoke(app, ["validate", "vdnc"], input=str(issue_id) +
                           "\n"+name+"\n"+namespace+"\n"+branch+"\n")
    result = result.output
    result = result.split("branch")[1]
    result = result.strip("\n")[1:]
    assert result == "136-fastjson-Versiondetails.json exists"


def test_vdnc_with_invalid_id():
    """test with invlid id"""
    issue_id = 500
    name = "Koha"
    namespace = "pramit-d"
    branch = "Koha"

    result = runner.invoke(app, ["validate", "vdnc"], input = str(issue_id)+
                           "\n"+name+"\n"+namespace+"\n"+branch+"\n")
    result = result.output
    result = result.split("branch")[1]
    result = result.strip("\n")[1:]
    assert result == "Could not find issue with id : 500"

def test_vdnc_with_invalid_version_tag():
    """check version tag present under besecure issue details &
    the tag written inside the version details file is not same"""
    issue_id = 148
    name = "Koha"
    namespace = "pramit-d"
    branch = "Koha"

    result = runner.invoke(app, ["validate", "vdnc"], input=str(
        issue_id)+"\n"+name+"\n"+namespace+"\n"+branch+"\n")
    result = result.output
    result = result.split("branch")[1]
    result = result.strip("\n")[1:]
    assert result == "Alert! Mismatch Version tag : Issue- "\
        "v21.05.18 & Versiondetails file- v21.05.17"

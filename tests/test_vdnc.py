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

    result = runner.invoke(app, ["validate", "version_file"], input=str(issue_id) +
                           "\n"+name+"\n"+namespace+"\n"+branch+"\n")
    result = result.output
    result = result.split("branch")[1]
    result = result.strip("\n")[1:]
    assert result == "136-fastjson-Versiondetails.json exists"


def test_vdnc_file_does_not_exists():
    """test with wrong/invalid file name"""
    issue_id = 405
    name = "OpenIDM"
    namespace = "pramit-d"
    branch = "main"

    result = runner.invoke(app, ["validate", "version_file"], input=str(issue_id) +
                           "\n"+name+"\n"+namespace+"\n"+branch+"\n")
    result = result.output
    result = result.split("branch")[1]
    result = result.strip("\n")[1:]
    assert result == "Alert! 405-OpenIDM-"\
        "Versiondetails.json does not exists"


def test_vdnc_with_invalid_id():
    """test with invlid id"""
    issue_id = 500
    name = "Koha"
    namespace = "pramit-d"
    branch = "Koha"

    result = runner.invoke(app, ["validate", "version_file"], input=str(issue_id) +
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

    result = runner.invoke(app, ["validate", "version_file"], input=str(
        issue_id)+"\n"+name+"\n"+namespace+"\n"+branch+"\n")
    result = result.output
    result = result.split("branch")[1]
    result = result.strip("\n")[1:]
    assert result == "Alert! Mismatch Version tag : Issue- "\
        "v21.05.18 & Versiondetails file- v21.05.17"


def test_vdnc_with_invalid_username():
    """test with invalid username"""
    issue_id = 136
    name = "fastjson"
    namespace = "prdut"
    branch = "main"

    result = runner.invoke(app, ["validate", "version_file"], input=str(issue_id) +
                           "\n"+name+"\n"+namespace+"\n"+branch+"\n")
    result = result.output
    result = result.split("branch")[1]
    result = result.strip("\n")[1:]
    assert result == "Alert! prdut is not valid username"


def test_vdnc_with_invalid_branch():
    """test with invalid branch name"""
    issue_id = 197
    name = "bit"
    namespace = "pramit-d"
    branch = "xyz"

    result = runner.invoke(app, ["validate", "version_file"], input=str(issue_id) +
                           "\n"+name+"\n"+namespace+"\n"+branch+"\n")
    result = result.output
    result = result.split("branch")[1]
    result = result.strip("\n")[1:]
    assert result == "Alert! xyz does not "\
        "exists under besecure-osspoi-datastore for pramit-d"


def test_vdnc_with_invalid_repo():
    """besecure-osspoi-datastore does not exists under mentioned user"""
    issue_id = 197
    name = "bit"
    namespace = "arunpillai6"
    branch = "main"

    result = runner.invoke(app, ["validate", "version_file"], input=str(issue_id) +
                           "\n"+name+"\n"+namespace+"\n"+branch+"\n")
    result = result.output
    result = result.split("branch")[1]
    result = result.strip("\n")[1:]
    assert result == "Alert! Could not find "\
        "besecure-osspoi-datastore under arunpillai6"


def test_vdnc_with_wrong_project():
    """besecure-osspoi-datastore does not exists under mentioned user"""
    issue_id = 197
    name = "Koha"
    namespace = "Be-Secure"
    branch = "main"

    result = runner.invoke(app, ["validate", "version_file"], input=str(issue_id) +
                           "\n"+name+"\n"+namespace+"\n"+branch+"\n")
    result = result.output
    result = result.split("branch")[1]
    result = result.strip("\n").replace("\n", "")[1:]
    assert result == "Alert! Mismatch issue_id-project :  "\
        "Issue id 197 does not match the project Koha"


def test_vdnc_with_invalid_project():
    """project does not exists under Be-Secure"""
    issue_id = 197
    name = "bitttt"
    namespace = "Be-Secure"
    branch = "main"

    result = runner.invoke(app, ["validate", "version_file"], input=str(issue_id) +
                           "\n"+name+"\n"+namespace+"\n"+branch+"\n")
    result = result.output
    result = result.split("branch")[1]
    result = result.strip("\n")[1:]
    assert result == "Could not find bitttt under Be-Secure"


def test_vdnc_check_under_OSSPMaster():
    """check if mentioned project exists under OSSP-master.json file"""
    issue_id = 405
    name = "OpenIDM"
    namespace = "pramit-d"
    branch = "test-dev-kit"

    result = runner.invoke(app, ["validate", "version_file"], input=str(issue_id) +
                           "\n"+name+"\n"+namespace+"\n"+branch+"\n")
    result = result.output
    result = result.split("branch")[1]
    result = result.strip("\n")[1:]
    assert result == "Alert! OpenIDM does not exists "\
        "under besecure-osspoi-datastore"

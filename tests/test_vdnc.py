from typer.testing import CliRunner
from besecure_developer_toolkit.cli import app

runner = CliRunner()

## test with valid data
def test_vdnc():
    id = 136
    name = "fastjson"
    namespace = "Be-Secure"
    branch = "main"
    
    result = runner.invoke(app, ["validate", "vdnc"], input=str(id)+"\n"+name+"\n"+namespace+"\n"+branch+"\n")
    result = result.output
    a = result.split("branch")[1]
    a = a.strip("\n")[1:]
    assert a == "136-fastjson-Versiondetails.json exists"

## test with invlid id
def test_vdnc_with_invalid_id():
    id = 500
    name = "Koha"
    namespace = "pramit-d"
    branch = "Koha"
    
    result = runner.invoke(app, ["validate", "vdnc"], input=str(id)+"\n"+name+"\n"+namespace+"\n"+branch+"\n")
    result = result.output
    a = result.split("branch")[1]
    a = a.strip("\n")[1:]
    assert a == "Could not find issue with id : 500"

## check the version tag in issue is same as the one inside the version details file
def test_vdnc_with_invalid_version_tag():
    id = 148
    name = "Koha"
    namespace = "pramit-d"
    branch = "Koha"
    
    result = runner.invoke(app, ["validate", "vdnc"], input=str(id)+"\n"+name+"\n"+namespace+"\n"+branch+"\n")
    result = result.output
    a = result.split("branch")[1]
    a = a.strip("\n")[1:]
    assert a == "Alert! Mismatch Version tag : Issue- v21.05.18 & Versiondetails file- v21.05.17" 
from typer.testing import CliRunner

from besecure_developer_toolkit.cli import app

runner = CliRunner()

def test_metadata():
    id = "136"
    name = "fastjson"
    version = "1.2.24"
    result = runner.invoke(app, ["generate", "metadata"], input=id+"\n"+name+"\n")
    assert result.exit_code == 0
    assert f"Successfully generated metadata for {id}-{name}\n" in result.stdout
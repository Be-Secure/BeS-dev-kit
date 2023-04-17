from typer.testing import CliRunner

from besecure_developer_toolkit import __app_name__, __version__, cli

runner = CliRunner()

def test_version():
    result = runner.invoke(cli.app, ["-v"])
    assert result.exit_code == 0
    assert f"{__app_name__} v{__version__}\n" in result.stdout
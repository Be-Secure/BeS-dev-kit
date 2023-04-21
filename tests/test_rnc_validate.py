from typer.testing import CliRunner

runner = CliRunner()

def rnc_validate():
    OSSP_name = "Koha"
    OSSP_version = "v21"
    namespace = "pramit-d"
    branch = "Koha"
    report = "scorecard"

    
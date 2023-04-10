"""Be-Secure Developer Toolkit entry point script."""
from besecure_developer_toolkit import cli, __app_name__

def main():
    
    cli.app(prog_name=__app_name__)

if __name__ == "__main__":
    main()
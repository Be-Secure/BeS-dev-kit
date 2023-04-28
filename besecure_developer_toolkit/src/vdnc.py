"""vdnc validate"""
import sys
import json
from urllib.error import HTTPError
from urllib.request import urlopen
from rich import print
from besecure_developer_toolkit.src.create_ossp_master import OSSPMaster


class VdncValidate():
    """version details file naming convention validation class"""

    def __init__(self, issue_id: int, name: str, namespace: str, branch: str):
        self.issue_id = issue_id
        self.name = name
        self.namespace = namespace
        self.branch = branch

    def check_username(self):
        """This method checks if given username is valid or not"""
        try:
            urlopen("https://api.github.com/users/"+self.namespace)
        except HTTPError:
            print(f"[bold red]Alert! [green]"
                  f"{self.namespace} is not valid username")
            sys.exit()

    def check_branch_exists(self):
        """This method checks if the branch is exists
        under besecure-osspoi-datastore for given user"""
        try:
            urlopen("https://api.github.com/repos/"+self.namespace +
                    "/besecure-osspoi-datastore/branches/"+self.branch)
        except HTTPError:
            print(f"[bold red]Alert! [green]{self.branch} does not "
                  f"exists under besecure-osspoi-"
                  f"datastore for {self.namespace}")
            sys.exit()

    def check_repo_exists(self, flag, namespace) -> None:
        """This is an overriding method of CreateOsspMaster class
        It checks if besecure-osspoi-datastore repo exists under the given user,
        here flag is used for differentiate between base & child class method"""
        try:
            if flag:
                urlopen("https://api.github.com/repos/" +
                        namespace+"/besecure-osspoi-datastore")
        except HTTPError:
            print(f"[bold red]Alert! [green]Could not find "
                  f"besecure-osspoi-datastore under {namespace}")
            sys.exit()

    def verify_versiondetails_name(self):
        """It checks the version details file naming
        convention that is uploaded by user"""
        obj = OSSPMaster(self.issue_id, self.name)
        obj.check_issue_exists(self.issue_id)
        obj.check_repo_exists(self.name)
        obj.check_issue_related_to_project()
        self.check_username()
        self.check_repo_exists(True, self.namespace)
        self.check_branch_exists()
        try:
            urlopen("https://raw.githubusercontent.com/"
                    + self.namespace+"/besecure-osspoi-datastore/"
                    + self.branch+"/version_details/"+str(self.issue_id)
                    + "-"+self.name+"-Versiondetails.json")
            print(f"{self.issue_id}-{self.name}-Versiondetails.json exists")
        except HTTPError:
            print(f"[bold red]Alert! [green]{self.issue_id}-{self.name}-"
                  f"Versiondetails.json does not exists")

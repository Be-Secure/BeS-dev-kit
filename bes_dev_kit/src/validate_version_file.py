"""Version details file validate"""
import sys
import json
from urllib.error import HTTPError
from urllib.request import urlopen
from rich import print
from bes_dev_kit.src.create_ossp_master import OSSPMaster


class VersionFileValidate():
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
                  f"{self.namespace} is not a valid username")
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
        if obj.check_issue_exists(self.issue_id) is False:
            print("[bold red]Alert! [green]Issue " +
                    f"[yellow]{self.issue_id} [green]does not exist")
            sys.exit(1)
        if obj.check_repo_exists(self.name) is False:
            print("[bold red]Alert! [green]Repo [yellow]" +
                  f"{self.name} [green]does not exist")
            sys.exit()
        obj.check_issue_related_to_project()
        self.check_username()
        self.check_repo_exists(True, self.namespace)
        self.check_branch_exists()
        try:
            version_data = json.loads(urlopen(
                "https://raw.githubusercontent.com/"
                + self.namespace + "/"
                "besecure-osspoi-datastore/"
                + self.branch + "/version_details/"
                + str(self.issue_id) + "-"
                + self.name +
                "-Versiondetails.json").read())
            self.check_version_tag(version_data)
            print(f"{self.issue_id}-{self.name}-Versiondetails.json exists")
        except HTTPError:
            print(f"[bold red]Alert! [green]{self.issue_id}-{self.name}-"
                  f"Versiondetails.json does not exists")

    def check_version_tag(self, version_data):
        """It checks if the version tag present in besecure issue is
        same as version tag of version details file uploaded by user"""
        # retrive issue version tag
        json_data = json.loads(
            urlopen(f'https://api.github.com/repos/Be-Secure/'
                    f'Be-Secure/issues/{self.issue_id}').read())
        issue_version_tag = json_data["body"]
        issue_version_tag = str(issue_version_tag).split("###")[1]
        issue_version_tag = issue_version_tag.strip().replace('\n', '')
        issue_version_tag = issue_version_tag.replace('\r', '')
        issue_version_tag = issue_version_tag.replace(
            'Version of the project', '')
        
        versiondetails_version_tag = version_data[0]["version"]
        versiondetails_version_tag = str(
            versiondetails_version_tag).replace("\n", "")
        # check version tag
        if issue_version_tag != versiondetails_version_tag:
            print(f"[bold red]Alert! [yellow]Mismatch "
                "Version tag : [green]Issue- "
                f"{issue_version_tag} & Versiondetails"
                f" file- {versiondetails_version_tag}")
            sys.exit(1)
import json, sys, os
from rich import print
from urllib.request import urlopen
from besecure_developer_toolkit.src.CreateOsspMaster import OSSPMaster

class vdnc_validate():
    def __init__(self, id: int, name: str, namespace: str, branch: str):
        self.id = id
        self.name = name
        self.namespace = namespace
        self.branch = branch

    def check_username(self):
        try:
            urlopen("https://api.github.com/users/"+self.namespace)
        except:
            print (f"[bold red]Alert! [green]{self.namespace} is not valid username")
            sys.exit()

    def check_branch_exists(self):
        try:
            urlopen("https://api.github.com/repos/"+self.namespace+"/besecure-osspoi-datastore/branches/"+self.branch)
        except:
            print(f"[bold red]Alert! [green]{self.branch} does not exists under besecure-osspoi-datastore repo")
            sys.exit()
            
    def check_repo_exists(self,name, namespace) -> None:
        try:
            urlopen("https://api.github.com/repos/"+namespace+"/besecure-osspoi-datastore")
        except Exception as e:
            print(f"[bold red]Alert! [green]Could not find besecure-osspoi-datastore under {namespace}")
            sys.exit()

    def verify_versiondetails_name(self):
        obj = OSSPMaster(self.id, self.name)
        obj.check_issue_exists(self.id)
        obj.check_repo_exists(self.name)
        obj.check_issue_related_to_project()
        self.check_username()
        self.check_repo_exists(self.name,self.namespace)
        self.check_branch_exists()
        
        try:
            urlopen("https://raw.githubusercontent.com/"+self.namespace+"/besecure-osspoi-datastore/"+self.branch+"/version_details/"+str(self.id)+"-"+self.name+"-Versiondetails.json")
            print(f"{self.id}-{self.name}-Versiondetails.json exists")
        except:
            print(f"[bold red]Alert! [green]{self.id}-{self.name}-Versiondetails.json does not exists")
        


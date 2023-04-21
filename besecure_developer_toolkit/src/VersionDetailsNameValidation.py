import sys,json
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

    ## check the version tag in issue is same as the one inside the version details file
    def check_version_tag_exists(self):
        # retrive issue version tag 
        json_data = json.loads(urlopen(f'https://api.github.com/repos/Be-Secure/Be-Secure/issues/{self.id}').read())
        issue_version_tag = json_data["body"]
        issue_version_tag = str(issue_version_tag).split("###")[1]
        issue_version_tag=issue_version_tag.strip().replace('\n', '').replace('\r', '').replace('Version of the project','').strip()

        # retrive versiondetails version tag
        json_data = json.loads(urlopen("https://raw.githubusercontent.com/"+self.namespace+"/besecure-osspoi-datastore/"+self.branch+"/version_details/"+str(self.id)+"-"+self.name+"-Versiondetails.json").read())
        versiondetails_version_tag = json_data[0]["version"]
        versiondetails_version_tag = str(versiondetails_version_tag).replace("\n", "")
        # check version tag
        if issue_version_tag != versiondetails_version_tag:
            print(f"[bold red]Alert! [yellow]Mismatch Version tag : [green]Issue- {issue_version_tag} & Versiondetails file- {versiondetails_version_tag}")
            return False
        else:
            return True
        

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
            val = self.check_version_tag_exists()
            if val:
                print(f"{self.id}-{self.name}-Versiondetails.json exists")
        except:
            print(f"[bold red]Alert! [green]{self.id}-{self.name}-Versiondetails.json does not exists")
        
        


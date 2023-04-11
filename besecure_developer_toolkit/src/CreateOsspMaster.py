import sys, os, json, subprocess
from urllib.request import urlopen
from rich import print

class OSSPMaster():
    
    def __init__(self, id: int, name: str) -> None:
        self.id = id
        self.name = name
    
    def check_issue_exists(self,id) -> None:
        try:
            urlopen('https://github.com/Be-Secure/Be-Secure/issues/'+str(id))
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            print("Could not find issue with id : "+id)
            sys.exit()
    
    def check_repo_exists(self,name) -> None:
        try:
            urlopen('https://api.github.com/repos/Be-Secure/'+name)
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            print("Could not find "+ name +" under Be-Secure")
            sys.exit()
    
    def write_tech_stack(self,bes_id):
        raw_data = urlopen("https://api.github.com/repos/Be-Secure/Be-Secure/issues/"+str(bes_id))

        data = json.loads(raw_data.read())

        body_data = iter(data["body"].splitlines())
        found = "false"
        for i in body_data:
            if i == "### Tech Stack":
                found = "true"
                continue
            if len(i.strip()) == 0:
                continue
            if len(i.strip()) != 0 and found == "true":
                s = str(i.split(" [")[1])
                s = str(s.split("]")[0])
                break    
        return s
    def write_project_repos_data(self,project_data):
        project_repos = {
        "main_github_url": "",
        "main_bes_url": "",
        "all_projects": [                                                                        
            {
                "id": 0,
                "name": "",
                "url": ""
            }
        ],
        "all_bes_repos": [                                                                  
            {
                "id": 0,
                "name": "",
                "url": ""
            }
                    
        ]
        }
        project_repos.update({"main_github_url": project_data["parent"]["html_url"]}) 
        project_repos.update({"main_bes_url": project_data["html_url"]})
        project_repos["all_projects"][0]["id"] = project_data["parent"]["id"]     
        project_repos["all_projects"][0]["name"] = project_data["parent"]["full_name"]
        project_repos["all_projects"][0]["url"] = project_data["parent"]["html_url"]
        project_repos["all_bes_repos"][0]["id"] = project_data["id"]
        project_repos["all_bes_repos"][0]["name"] = project_data["full_name"]
        project_repos["all_bes_repos"][0]["url"] = project_data["html_url"]         
        return project_repos

    def write_tags(self, bes_id):
        url = 'https://api.github.com/repos/Be-Secure/Be-Secure/issues/'+str(bes_id)+'/labels'
        tags_json_data = urlopen(url)
        tags_dict = json.loads(tags_json_data.read())
        tags = []
        for i in range(len(tags_dict)):
            tags.append(tags_dict[i]["name"])
        return tags
    
    def write_languages(self,name):
        raw_data = urlopen("https://api.github.com/repos/Be-Secure/"+name+"/languages")
        data = json.loads(raw_data.read())
        return data
    
    def write_to_ossp_master(self, f, ossp_master_json, data, overwrite: bool):
            if overwrite:
                for i in range(len(ossp_master_json["items"])):
                    if ossp_master_json["items"][i]["id"] == self.id:
                        ossp_master_json["items"][i] = data
                        break
            else:    
                ossp_master_json["items"].append(data)
            f.seek(0)
            f.write(json.dumps(ossp_master_json, indent=4))
            f.truncate()
        
    
    
    def GenerateOsspMaster(self, overwrite: bool):
        self.check_issue_exists(self.id)
        self.check_repo_exists(self.name)
        osspoi_dir = os.environ['OSSPOI_DIR']
        namespace = os.environ['GITHUB_ORG']
        token = os.environ['GITHUB_AUTH_TOKEN']
        write_flag = True
        f = open(osspoi_dir+"/OSSP-Master.json", "r+")
        ossp_master_json = json.load(f)
        if not overwrite:                 
            for i in range(len(ossp_master_json["items"])):
                if ossp_master_json["items"][i]["id"] == self.id:
                    print("[bold red]Alert! [green]Entry for "+str(self.id)+"-"+self.name+" already present")
                    write_flag = False
                    break
                else:
                    write_flag = True
        if write_flag:
            # proc = subprocess.Popen([f'curl -L -H "Accept: application/vnd.github+json" -H "Authorization: Bearer <YOUR-TOKEN>"-H "X-GitHub-Api-Version: 2022-11-28" https://api.github.com//{namespace}/{self.name}'], stdout=subprocess.PIPE, shell=True)
            # (out, err) = proc.communicate()
            url_data = urlopen('https://api.github.com/repos/Be-Secure/'+self.name)
            project_data = json.loads(url_data.read())
            ossp_data = json.loads('{}')
            repo_keys = [ "id", "bes_tracking_id", "issue_url", "name", "full_name", "description", "bes_technology_stack", "watchers_count", "forks_count", "stargazers_count", "size", "open_issues", "created_at", "updated_at", "pushed_at", "git_url", "clone_url", "html_url", "homepage", "owner", "project_repos", "license", "language", "tags" ]
            for i in repo_keys:
                if i == "id" or i == "bes_tracking_id":
                    ossp_data[i] = self.id
                elif i == "issue_url":
                    ossp_data[i] = 'https://github.com/Be-Secure/Be-Secure/issues/'+str(self.id)
                elif i == "bes_technology_stack":
                    ossp_data[i] = self.write_tech_stack(self.id)
                elif i == "project_repos":
                    ossp_data[i] = self.write_project_repos_data(project_data)
                elif i == "tags":
                    ossp_data[i] = self.write_tags(self.id)
                elif i == "language":
                    ossp_data[i] = self.write_languages(self.name)
                else:
                    ossp_data[i] = project_data[i]
            self.write_to_ossp_master(f, ossp_master_json, ossp_data, overwrite)
            f.close()        
        
        
    
    


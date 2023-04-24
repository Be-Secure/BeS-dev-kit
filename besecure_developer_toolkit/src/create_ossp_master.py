"""
    licence part todo
"""
import sys
import os
import json
from urllib.request import urlopen
from rich import print


class OSSPMaster():
    """
        Generate OSSPMaster report.
    """

    def __init__(self, issue_id: int, name: str) -> None:
        self.issue_id = issue_id
        self.name = name

    def check_issue_exists(self, issue_id) -> None:
        """
            Check for issue id is exits or not.
        """
        try:
            urlopen('https://github.com/Be-Secure/Be-Secure/issues/'+str(issue_id))
        except Exception as err:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            print(
                f"Could not find issue with id: {str(issue_id)}, error: {str(err)}")
            sys.exit()

    def check_issue_related_to_project(self):
        """
            Check project name from issue
        """
        json_data = json.loads(urlopen(
            f'https://api.github.com/repos/Be-Secure/Be-Secure/issues/{self.issue_id}').read())
        issue_title = json_data["title"]
        project_name = str(str(issue_title).split(":")[1]).replace(" ", "")
        if project_name != self.name:
            print(
                f"[bold red]Alert! [yellow]Mismatch issue_id-project : [green] \
                    Issue id {self.issue_id} does not match the project {self.name}")
            sys.exit()

    def check_repo_exists(self, name) -> None:
        """
            Check if repo exists in Be-Secure or not 
        """
        try:
            urlopen('https://api.github.com/repos/Be-Secure/'+name)
        except Exception as err:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            print(f"Could not find {name} under Be-Secure, Error: {err}")
            sys.exit()

    def write_tech_stack(self, bes_id):
        """
            Check the tech Stack of the Project
        """
        raw_data = urlopen(
            "https://api.github.com/repos/Be-Secure/Be-Secure/issues/"+str(bes_id))

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
                stack = str(i.split(" [")[1])
                stack = str(stack.split("]")[0])
                break
        return stack

    def write_project_repos_data(self, project_data):
        """
            Create json report for repository reletated content
            like: main_github_url, main_bes_url etc...
        """
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
        project_repos.update(
            {"main_github_url": project_data["parent"]["html_url"]})
        project_repos.update({"main_bes_url": project_data["html_url"]})
        project_repos["all_projects"][0]["id"] = project_data["parent"]["id"]
        project_repos["all_projects"][0]["name"] = project_data["parent"]["full_name"]
        project_repos["all_projects"][0]["url"] = project_data["parent"]["html_url"]
        project_repos["all_bes_repos"][0]["id"] = project_data["id"]
        project_repos["all_bes_repos"][0]["name"] = project_data["full_name"]
        project_repos["all_bes_repos"][0]["url"] = project_data["html_url"]
        return project_repos

    def write_tags(self, bes_id):
        """
            get the tags from github labels
        """
        url = 'https://api.github.com/repos/Be-Secure/Be-Secure/issues/' + \
            str(bes_id)+'/labels'
        tags_json_data = urlopen(url)
        tags_dict = json.loads(tags_json_data.read())
        tags = []
        for name in tags_dict:
            # todo: fixme
            tags.append(name)
        return tags

    def write_languages(self, name):
        """
            fetch the languages from github URL
        """
        raw_data = urlopen(
            "https://api.github.com/repos/Be-Secure/"+name+"/languages")
        data = json.loads(raw_data.read())
        return data

    def write_to_ossp_master(self, f, ossp_master_json, data, overwrite: bool):
        """
            Add or override the project details in ossp_master
        """
        if overwrite:
            for i in range(len(ossp_master_json["items"])):
                if ossp_master_json["items"][i]["id"] == self.issue_id:
                    ossp_master_json["items"][i] = data
                    break
        else:
            ossp_master_json["items"].append(data)
        f.seek(0)
        f.write(json.dumps(ossp_master_json, indent=4))
        f.truncate()

    def generate_ossp_master(self, overwrite: bool):
        """
            Generate ossp master json report
        """
        self.check_issue_exists(self.issue_id)
        self.check_repo_exists(self.name)
        self.check_issue_related_to_project()
        osspoi_dir = os.environ['OSSPOI_DIR']
        write_flag = True
        f = open(f"{osspoi_dir}/OSSP-Master.json", "r+", encoding="utf-8")
        ossp_master_json = json.load(f)
        if not overwrite:
            for i in range(len(ossp_master_json["items"])):
                if ossp_master_json["items"][i]["id"] == self.issue_id:
                    print("[bold red]Alert! [green]Entry for "+str(self.issue_id) +
                          "-"+self.name+" already present under OSSP-Master.json")
                    write_flag = False
                    break
                else:
                    write_flag = True
        if write_flag:
            url_data = urlopen(
                f'https://api.github.com/repos/Be-Secure/{self.name}')
            project_data = json.loads(url_data.read())
            ossp_data = json.loads('{}')
            repo_keys = ["id", "bes_tracking_id", "issue_url", "name",
                          "full_name", "description", "bes_technology_stack",
                          "watchers_count", "forks_count", "stargazers_count",
                          "size", "open_issues", "created_at", "updated_at",
                          "pushed_at", "git_url", "clone_url", "html_url",
                          "homepage", "owner", "project_repos", "license",
                          "language", "tags"
                        ]
            for i in repo_keys:
                if i == "id" or i == "bes_tracking_id":
                    ossp_data[i] = self.issue_id
                elif i == "issue_url":
                    ossp_data[i] = 'https://github.com/Be-Secure/Be-Secure/issues/' + \
                        str(self.issue_id)
                elif i == "bes_technology_stack":
                    ossp_data[i] = self.write_tech_stack(self.issue_id)
                elif i == "project_repos":
                    ossp_data[i] = self.write_project_repos_data(project_data)
                elif i == "tags":
                    ossp_data[i] = self.write_tags(self.issue_id)
                elif i == "language":
                    ossp_data[i] = self.write_languages(self.name)
                else:
                    ossp_data[i] = project_data[i]
            self.write_to_ossp_master(
                f, ossp_master_json, ossp_data, overwrite)
            f.close()

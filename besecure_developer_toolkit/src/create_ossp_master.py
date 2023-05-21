"""
    licence part todo
"""
import sys
import os
import json
import urllib.request
import requests
from rich import print


class OSSPMaster():
    """
        Generate OSSPMaster report.
    """

    def __init__(self, issue_id: int, name: str) -> None:
        self.issue_id = issue_id
        self.name = name

    @staticmethod
    def check_issue_exists(issue_id: int):
        """Function to check if the issue exists

        Args:
            issue_id (int): Issue issue_id

        Returns:
            bool: True if issue exists and False if otherwise
        """
        url = f"https://api.github.com/repos/Be-Secure/Be-Secure/issues/{issue_id}"
        try:
            response = requests.head(url, timeout=10)
            if response.status_code == 403:
                print(f'[red bold]Alert! [yellow]'\
                    'GitHub API rate limit '\
                    'exceeded for this system')
                sys.exit(1)
            return response.status_code < 400
        except requests.exceptions.RequestException as exc:
            print(response.text)
            print(exc)
            return False

    def check_issue_related_to_project(self):
        """
            Check project name from issue
        """
        url = f'https://api.github.com/repos/Be-Secure/Be-Secure/issues/{self.issue_id}'
        with urllib.request.urlopen(url) as raw_data:
            json_data = json.loads(raw_data.read())
            issue_title = json_data["title"]
            project_name = str(str(issue_title).split(":")[1]).replace(" ", "")
            if project_name != self.name:
                print("[bold red]Alert![yellow] Mismatch issue_id-project:" +
                        f"[green] Issue id {self.issue_id} " +
                        f"does not match the project {self.name}")
                sys.exit()

    @staticmethod
    def check_repo_exists(name: str):
        """Checks if the repo exists

        Args:
            name (str): Project name
        """
        url = f"https://api.github.com/repos/Be-Secure/{name}"
        try:
            response = requests.head(url, timeout=10)
            if response.status_code == 403:
                print(f'[red bold]Alert! [yellow]'\
                    'GitHub API rate limit '\
                    'exceeded for this system')
                sys.exit(1)
            return response.status_code < 400
        except requests.exceptions.RequestException as exc:
            print(exc)
            return False

    def write_tech_stack(self, bes_id):
        """
            Check the tech Stack of the Project
        """
        url = f"https://api.github.com/repos/Be-Secure/Be-Secure/issues/{str(bes_id)}"
        with urllib.request.urlopen(url) as raw_data:
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
                    stack = str(stack.split("]", maxsplit=1)[0])
                    break
        return stack

    def write_project_repos_data(self, project_data):
        """
            Create json report for repository related content
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
        with urllib.request.urlopen(url) as tags_json_data:
            tags_dict = json.loads(tags_json_data.read())
            tags = []
            # pylint: disable=unused-variable
            for i, tag_name in enumerate(tags_dict):
                tags.append(tag_name["name"])
            return tags

    def write_languages(self, name):
        """
            fetch the languages from github URL
        """
        url = f"https://api.github.com/repos/Be-Secure/{name}/languages"
        with urllib.request.urlopen(url) as raw_data:
            data = json.loads(raw_data.read())
        return data

    def write_to_ossp_master(self, file_pointer, ossp_master_json, data, overwrite: bool):
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
        file_pointer.seek(0)
        file_pointer.write(json.dumps(ossp_master_json, indent=4))
        file_pointer.truncate()
        if overwrite:
            print("[bold red]Alert! [green]Data for " +
                f"[yellow]{self.name} [green] in OSSP-Master.json has been overwritten")
        else:
            print("[bold red]Alert! [green]Added " +
                f"[yellow]{self.name} [green]to OSSP-Master.json")


    def generate_ossp_master(self, overwrite: bool):
        """
            Generate ossp master json report
        """
        if self.check_issue_exists(self.issue_id) is False:
            print("[bold red]Alert! [green]Issue " +
                  f"[yellow]{self.issue_id} [green]does not exist")
            sys.exit()
        if self.check_repo_exists(self.name) is False:
            print("[bold red]Alert! [green]Repo [yellow]" +
                  f"{self.name} [green]does not exist")
            sys.exit()
        self.check_issue_related_to_project()
        osspoi_dir = os.environ['OSSPOI_DIR']
        write_flag = True
        with open(f"{osspoi_dir}/OSSP-Master.json", "r+", encoding="utf-8") as file_pointer:
            ossp_master_json = json.load(file_pointer)
            if not overwrite:
                for i in range(len(ossp_master_json["items"])):
                    if ossp_master_json["items"][i]["id"] == self.issue_id:
                        print("[bold red]Alert! [green]Entry for "+str(self.issue_id) +
                            "-"+self.name+" already present under OSSP-Master.json")
                        write_flag = False
                        break
            if write_flag:
                url = f"https://api.github.com/repos/Be-Secure/{self.name}"
                with urllib.request.urlopen(url) as url_data:
                    project_data = json.loads(url_data.read())
                ossp_data = json.loads('{}')
                repo_keys = [
                    "id", "bes_tracking_id", "issue_url", "name",
                    "full_name", "description", "bes_technology_stack",
                    "watchers_count", "forks_count", "stargazers_count",
                    "size", "open_issues", "created_at", "updated_at",
                    "pushed_at", "git_url", "clone_url", "html_url",
                    "homepage", "owner", "project_repos", "license",
                    "language", "tags"
                ]
                for i in repo_keys:
                    if i in ('id', 'bes_tracking_id'):
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
                    file_pointer, ossp_master_json, ossp_data, overwrite)
            file_pointer.close()

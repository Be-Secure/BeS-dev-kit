import requests
import json
import os

class OsspoiMaster():

    def __init__(self) -> None:
        pass

    def tec_stack(self, bes_id):
        try:
            loadJson = json.loads(requests.get("https://api.github.com/repos/Be-Secure/Be-Secure/issues/"+bes_id).text)
        except Exception as e:
            raise f"Fails to fetch the json report for issue error: {e}"
        lableToFind = {"L&F": True, "A": True, "DA": True, "S": True, "DO": True}
        for label in loadJson["labels"]:
            try:
                if (lableToFind[label["name"]] == True):
                    return label["name"]
            except Exception as e:
                pass

    def languages(self, name):
        try:
            loadJson = json.loads(requests.get(f"https://api.github.com/repos/Be-Secure/{name}/languages").text)
            return loadJson
        except Exception as e:
            raise f"Fails to fetch the tags for issue error: {e}"
        
    def tags(self, bes_id):
        try:
            tags = []
            loadJson = json.loads(requests.get(f"https://api.github.com/repos/Be-Secure/Be-Secure/issues/{bes_id}/labels").text)
            for tag in loadJson:
                tags.append(tag["name"])
            return tags
        except Exception as e:
            raise f"Fails to fetch the tags for issue error: {e}"
        
    def appendToFile(self, data, besecureOsspoi, beSecureID):
        try:
            found = True
            systemPath = os.path.join(besecureOsspoi, "OSSP-Master.json")
            fileR = open(systemPath, "r+")
            fileRead = json.load(fileR)
            for project in fileRead["items"]:
                if project["id"] == beSecureID:
                    project = data
                    found = False
                    break
            if found:
                fileRead["items"].append(data)
            fileWrite = open(systemPath, "w+")
            json.dump(fileRead, fileWrite, indent=2)
            fileWrite.close()
        except Exception as e:
            raise f"Fails to read content error: {e}"



    def createJsonForOsspoiMaster(self, name, id, besecureOsspoi):
        try:
            loadJson = json.loads(requests.get("https://api.github.com/repos/Be-Secure/"+name).text)
        except Exception as e:
            raise f"Fails to fetch the json report error: {e}"
        label = self.tec_stack(id)
        data = {
            "id": loadJson["id"],
            "bes_tracking_id": id,
            "issue_url": f"https://github.com/BeSecure/Be-Secure/issues/{id}",
            name: name,
            "full_name": loadJson["full_name"],
            "description": loadJson["description"],
            "bes_technology_stack": label,
            "watchers_count": loadJson["watchers_count"],
            "forks_count": loadJson["forks_count"],
            "stargazers_count": loadJson["stargazers_count"],
            "size": loadJson["size"],
            "open_issues": loadJson["open_issues"],
            "created_at": loadJson["created_at"],
            "updated_at": loadJson["updated_at"],
            "pushed_at": loadJson["pushed_at"],
            "git_url": loadJson["git_url"],
            "clone_url": loadJson["clone_url"],
            "html_url": loadJson["html_url"],
            "homepage": loadJson["homepage"],
            "owner": loadJson["owner"],
            "project_repos": {
                "main_github_url": loadJson["parent"]["html_url"],
                "main_bes_url": loadJson["html_url"],
                "all_projects": [
                    {
                        "id": loadJson["parent"]["id"],
                        "name": loadJson["parent"]["full_name"],
                        "url": loadJson["parent"]["html_url"],
                    }
                    ],
                    "all_bes_repos": [
                    {
                        "id": id,
                        "name": loadJson["full_name"],
                        "url": loadJson["html_url"]
                    }
                ]
            },
            "license": loadJson["license"],
            "language": self.languages(name),
            "tags": self.tags(id)

        }
        self.appendToFile(data, besecureOsspoi, id)
        return data
        


osspoiMaster = OsspoiMaster()
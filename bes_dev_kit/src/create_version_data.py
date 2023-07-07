"""
    licence part todo
"""
import os
import json
import datetime
import subprocess
import shutil
import urllib.request
from rich import print


class Version():
    """
        create version details page
    """

    def __init__(self, issue_id: int, name: str):
        self.issue_id = issue_id
        self.name = name

    def get_version_tag(self, bes_id):
        """
            fetch the version of the project
        """
        url = f"https://api.github.com/repos/Be-Secure/Be-Secure/issues/{str(bes_id)}"
        with urllib.request.urlopen(url) as raw_data:
            data = json.loads(raw_data.read())
            body_data = iter(data["body"].splitlines())
            found = "false"
            for i in body_data:
                if i == "### Version of the project":
                    found = "true"
                    continue
                if len(i.strip()) == 0:
                    continue
                if len(i.strip()) != 0 and found == "true":
                    break
        return str(i)

    def get_release_date(self, version, name):
        """Get release date of project

        Args:
            version (str): project version
            name (str): project name

        Returns:
            str: date in dd-mmm-yyy format
        """
        self.cleanup()
        os.system('git clone -q https://github.com/Be-Secure/' +
                  name + ' /tmp/'+name)
        os.chdir('/tmp/'+name)
        proc = subprocess.Popen([
            'git log --tags --simplify-by-decoration --pretty="format:%ci %d" | grep -w "' +
            version + '"'
        ], stdout=subprocess.PIPE, shell=True)
        (out) = proc.communicate()
        try:
            date = str(out).split(" ", maxsplit=1)[0]
            raw_date = date.split("'")[1]
            split_date = raw_date.split("-")
            yyyy = int(split_date[0])
            mmm = int(split_date[1])
            dd = int(split_date[2])
            format_datetime = datetime.datetime(yyyy, mmm, dd)
            final_date = str(format_datetime.strftime("%d-%b-%Y"))
            return final_date
        except ValueError:
            print(f"Version {version} not found, ignoring release date")

    def cleanup(self):
        """
            remove the file/directory from tmp
        """
        if os.path.exists(f'/tmp/{self.name}'):
            shutil.rmtree('/tmp/'+self.name)

    def overwrite_version_data(self, file_pointer, version_data_new, original_data, version_tag):
        """
            overwrite the version data for the specific version.
        """
        for i in range(len(original_data)):
            # Fixme
            if original_data[i]["version"] == version_tag:
                original_data[i] = version_data_new
                break
        file_pointer.seek(0)
        file_pointer.write(json.dumps(original_data, indent=4))
        file_pointer.truncate()
        print("[bold red]Alert! [green]Version data for " +
              f"[yellow]{self.name} {version_tag} [green]has been overwritten")

    def generate_version_data(self, overwrite: bool):
        """
            generate version details page in osspoi_datastore
        """
        osspoi_dir = os.environ['OSSPOI_DIR']
        version_data_new = {
            "version": "",
            "release_date": "",
            "criticality_score": "Not Available",
            "scorecard": "Not Available",
            "cve_details": "Not Available"
        }
        write_flag = True
        version_tag = self.get_version_tag(self.issue_id)
        version_data_new["version"] = version_tag
        date = self.get_release_date(version_tag, self.name)
        if date is None:
            version_data_new["release_date"] = "Not Available"
        else:
            version_data_new["release_date"] = date
        path = osspoi_dir+"/version_details/" + \
            str(self.issue_id) + "-" + self.name + "-" "Versiondetails.json"
        if os.path.exists(path):
            with open(path, "r+", encoding="utf-8") as file_pointer:
                original_data = json.load(file_pointer)
                for i in range(len(original_data)):
                    # Fixme
                    if original_data[i]["version"] == version_data_new["version"] and not overwrite:
                        write_flag = False
                        alert = "[bold red]Alert! [green]Version"
                        message = f"{alert} {version_tag} exists under"
                        name = f"{self.issue_id}-{self.name}-Versiondetails.json"
                        print(f"{message} {name}")
                        break
                if write_flag and not overwrite:
                    original_data.append(version_data_new)
                    file_pointer.seek(0)
                    file_pointer.write(json.dumps(original_data, indent=4))
                    file_pointer.truncate()
                    print("[bold red]Alert! [green]Appending details for [yellow]{self.name}" +
                          f"{version_tag} into [yellow] {path}")
                elif write_flag and overwrite:
                    self.overwrite_version_data(
                        file_pointer, version_data_new, original_data, version_tag)
                else:
                    pass
        else:
            with open(path, "w", encoding="utf-8") as file:
                data = []
                data.append(version_data_new)
                file.write(json.dumps(data, indent=4))
                print("[bold red]Alert! [green]Created version details file for" +
                      f"[yellow] {self.issue_id}-{self.name} "+
                      f"[green]with version:[yellow]{version_tag}")
        self.cleanup()

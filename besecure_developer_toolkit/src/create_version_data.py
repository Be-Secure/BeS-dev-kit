"""
    licence part todo
"""
import os
import json
import datetime
import subprocess
import shutil
from urllib.request import urlopen
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
        raw_data = urlopen(
            f"https://api.github.com/repos/Be-Secure/Be-Secure/issues/{str(bes_id)}")
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
        """
            fetch the release data of tracking project
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
        date = str(out).split(" ")[0]
        raw_date = date.split("'")[1]
        split_date = raw_date.split("-")
        format_datetime = datetime.datetime(
            int(split_date[0]), int(split_date[1]), int(split_date[2]))
        final_date = str(format_datetime.strftime("%d-%b-%Y"))
        return final_date

    def cleanup(self):
        """
            remove the file/directory from tmp
        """
        if os.path.exists(f'/tmp/{self.name}'):
            shutil.rmtree('/tmp/'+self.name)

    def overwrite_version_data(self, f, version_data_new, original_data, version_tag):
        """
            overwrite the version data for the specific version.
        """
        for i in range(len(original_data)):
            # Fixme
            if original_data[i]["version"] == version_tag:
                original_data[i] = version_data_new
                break
        f.seek(0)
        f.write(json.dumps(original_data, indent=4))
        f.truncate()

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
        version_tag = self.get_version_tag(self.issue_id)
        version_data_new["version"] = version_tag
        date = self.get_release_date(version_tag, self.name)
        version_data_new["release_date"] = date
        path = osspoi_dir+"/version_details/" + \
            str(self.issue_id) + "-" + self.name + "-" "Versiondetails.json"
        if os.path.exists(path):
            f = open(path, "r+", encoding="utf-8")
            original_data = json.load(f)
            for i in range(len(original_data)):
                # Fixme
                if original_data[i]["version"] == version_data_new["version"] and not overwrite:
                    write_flag = False
                    alert = "[bold red]Alert! [green]Version"
                    message = f"{alert} {version_tag} exists under"
                    name = f"{self.issue_id}-{self.name}-Versiondetails.json"
                    print(f"{message} {name}")
                    break
                else:
                    write_flag = True
            if write_flag and not overwrite:
                original_data.append(version_data_new)
                f.seek(0)
                f.write(json.dumps(original_data, indent=4))
                f.truncate()
            elif write_flag and overwrite:
                self.overwrite_version_data(
                    f, version_data_new, original_data, version_tag)
            else:
                pass
        else:
            f = open(path, "w", encoding="utf-8")
            f.write(json.dumps(version_data_new, indent=4))
        self.cleanup()
        f.close()

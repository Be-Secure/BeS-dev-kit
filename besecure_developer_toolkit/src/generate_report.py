"""
    licence part todo
"""
import json
import sys
import os
from urllib.request import urlopen
from rich import print


class Report():
    """
        Create report for scorcard, codeQl, and criticality_score
    """
    def __init__(self, issue_id: int, name: str, version: str, report: str):
        self.issue_id = issue_id
        self.name = name
        self.report = report
        self.version = version

    def fetch_report(self, url):
        """
            create json report for criticality_score, codeql, and scorecard
        """
        if self.report == "criticality_score":
            os.system('criticality_score --repo '+url +
                      ' --format json >> /tmp/'+self.report+'.json')
            f_critical = open('/tmp/'+self.report+'.json', 'r', encoding="utf-8")
            data = json.load(f_critical)
            f_critical.close()
        elif self.report == "codeql":
            token = os.environ['GITHUB_AUTH_TOKEN']
            cmd = 'curl -s -L -H "Accept: application/vnd.github+json" \
                -H "Authorization: Bearer ' + \
                token+'" -H "X-GitHub-Api-Version: 2022-11-28" '+url
            os.system(cmd+' >> /tmp/'+self.report+'.json')
            codeql_f = open('/tmp/'+self.report+'.json', 'r', encoding="utf-8")
            data = json.load(codeql_f)
            codeql_f.close()
        else:
            try:
                raw_data = urlopen(url)
            except Exception as err:
                exc_type, exc_obj, exc_tb = sys.exc_info()
                fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                print(exc_type, fname, exc_tb.tb_lineno)
                sys.exit(str(err))
            data = json.loads(raw_data.read())

        return data

    def write_report(self, data):
        """
            create report for criticality_score, codeql, and scorecard
            in assesment data store
        """
        assessment_dir = os.environ['ASSESSMENT_DIR']
        if self.report == "codeql":
            path = assessment_dir+'/'+self.name+'/'+self.version+'/sast'
        else:
            path = assessment_dir+'/'+self.name+'/'+self.version+'/'+self.report
        try:
            os.makedirs(path, exist_ok=True)
        except FileExistsError as err:
            print(f"error to create file Error: {err}")
        file = f"{path}/{self.name}-{self.version}-{self.report}-report.json"
        f = open(file, "w", encoding="utf-8")
        f.write(json.dumps(data, indent=4))
        print(f"[bold red]Alert! [green]Added [yellow]{file}")

    def update_version_data(self):
        """
            provide versiondetails for version and read from assessment data store
        """
        osspoi_dir = os.environ['OSSPOI_DIR']
        assessment_dir = os.environ['ASSESSMENT_DIR']
        report_file = open(assessment_dir+'/'+self.name+'/'+self.version+'/'+self.report +
                            '/'+self.name + '-' + self.version +
                            '-' + self.report + '-report.json', "r", encoding="utf-8")
        version_file = open(osspoi_dir+"/version_details/"+str(self.issue_id) +
                            "-" + self.name + "-" "Versiondetails.json", "r+", encoding="utf-8")

        score_data = json.load(report_file)
        if self.report == "scorecard":
            score = score_data["score"]
        elif self.report == "criticality_score":
            score = score_data["criticality_score"]

        version_data = json.load(version_file)
        for i in range(len(version_data)):
            # Fixme
            if version_data[i]["version"] == self.version:
                version_data[i][self.report] = score
        version_file.seek(0)
        version_file.write(json.dumps(version_data, indent=4))
        version_file.truncate()
        report_file.close()
        version_file.close()

    def cleanup(self):
        """
            remove file from tmp
        """
        if self.report != "scorecard":
            os.remove('/tmp/'+self.report+'.json')

    def main(self):
        """
            generate report for scorecard, criticality_score amd codeql
        """
        if self.report == "scorecard":
            url = "https://api.securityscorecards.dev/projects/github.com/Be-Secure/"+self.name

        elif self.report == "criticality_score":
            if "GITHUB_AUTH_TOKEN" not in os.environ:
                print(
                    "[bold red] Alert! [green] Please use the below \
                          command to set your personal access token and try again.")
                print("[yellow]export GITHUB_AUTH_TOKEN=token")
                sys.exit()
            url = 'github.com/Be-Secure/'+self.name

        elif self.report == "codeql":
            if "GITHUB_AUTH_TOKEN" not in os.environ:
                print(
                    "[bold red] Alert! [green] Please use the \
                        below command to set your personal access token and try again.")
                print("[yellow]export GITHUB_AUTH_TOKEN=token")
                sys.exit()
            url = 'https://api.github.com/repos/Be-Secure/' + \
                self.name + '/code-scanning/alerts?tool_name=CodeQL'

        data = self.fetch_report(url)
        self.write_report(data)
        self.cleanup()

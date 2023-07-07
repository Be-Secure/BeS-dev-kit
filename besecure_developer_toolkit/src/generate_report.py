"""
    licence part todo
"""
import json
import csv
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
        self.flag = True

    def csv_to_json(self, csv_file_path, json_file_path):
        '''
            convert csv data to json data
        '''
        with open(csv_file_path, 'r') as csv_file:
            csv_data = csv.DictReader(csv_file)
            data_list = list(csv_data)
        with open(json_file_path, 'w') as json_file:
            json.dump(data_list, json_file, indent=4)

    def fetch_report(self, url):
        """
            create json report for criticality_score, codeql, and scorecard
        """
        if self.report == "criticality_score":
            command = 'criticality_score --repo ' + url + ' --format csv'
            json_file_path = '/tmp/' + self.name + '-' + self.version + '-' + self.report+'.json'
            csv_file_path = '/tmp/' + self.name + '-' + self.version + '-' + self.report+'.csv'
            command = command + f" > {csv_file_path} 2>/dev/null"
            os.system(command)
            self.csv_to_json(csv_file_path, json_file_path)
            f_critical = open(json_file_path, 'r', encoding="utf-8")
            data = json.load(f_critical)
            data = data[0]
            f_critical.close()
        elif self.report == "codeql":
            token = os.environ['GITHUB_AUTH_TOKEN']
            cmd = 'curl -s -L -H "Accept: application/vnd.github+json" \
                -H "Authorization: Bearer ' + \
                token+'" -H "X-GitHub-Api-Version: 2022-11-28" '+url
            os.system(cmd+' >> /tmp/' + self.name +
                       '-' + self.version + '-' +
                       self.report+'.json')
            codeql_f = open('/tmp/' + self.name +
                       '-' + self.version + '-' +
                       self.report+'.json', 'r', encoding="utf-8")
            data = json.load(codeql_f)
            codeql_f.close()
        elif self.report == 'sbom':
            self.flag = self.command_resp(os.system(url))
            if self.flag:
                try:
                    sbom_raw_data = open('/tmp/.sbom/sbom-output/_manifest/spdx_2.2/manifest.spdx.json', 'r', encoding="utf-8")
                    data = json.load(sbom_raw_data)
                    pack_len = len(data['packages'])
                    if pack_len == 1 and data['packages'][0]['name'] == self.name:
                        print('[bold red]There were no packages detected '
                            'during sbom report generation workflow')
                        self.flag = False
                    sbom_raw_data.close()
                except ValueError:
                    # includes simplejson.decoder.JSONDecodeError
                    print('[bold red]Decoding JSON has failed')
                    self.flag = False
                except FileNotFoundError:
                    print("[bold red]JSON file Not Found")
                    self.flag = False
            else:
                return
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
            create report for criticality_score, codeql, sbom and scorecard
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
        if self.report == 'sbom':
            if not self.flag:
                os.system('rm -rf /tmp/.sbom')
            else:
                os.system('rm -rf /tmp/.sbom/sbom-output')
                os.system('rm -rf /tmp/.sbom/' + self.name)
        elif self.report != "scorecard":
            os.system('rm -rf /tmp/' + self.name +
                       '-' + self.version +
                       '-' + self.report+'.*')

    def command_resp(self, return_val):
        if return_val == 0:
            return True and self.flag
        elif return_val == 1:
            return False and self.flag
    
    def setup_sbom(self):
        '''
            download & setup sbom tool
        '''
        if not os.path.exists('/tmp/.sbom/') and self.flag:
            self.flag = self.command_resp(os.system('mkdir /tmp/.sbom'))
        if not os.path.exists('/tmp/.sbom/sbom-tool-linux-x64') and self.flag:
            self.flag = self.command_resp(os.system('wget https://github.com/microsoft/sbom-tool/releases/download/v1.1.6/sbom-tool-linux-x64 -P /tmp/.sbom/'))
            self.flag = self.command_resp(os.system('chmod +x /tmp/.sbom/sbom-tool-linux-x64'))
        self.flag = self.command_resp(os.system('rm -rf /tmp/.sbom/sbom-output'))
        self.flag = self.command_resp(os.system('rm -rf /tmp/.sbom/' + self.name))
        self.flag = self.command_resp(os.system('mkdir /tmp/.sbom/sbom-output'))
        #clone ossp
        self.flag = self.command_resp(os.system('cd /tmp/.sbom && git clone --single-branch --branch ' + self.version + '_release https://github.com/Be-Secure/'+ self.name +'.git'))
        #sbom report command
        command = 'cd /tmp/.sbom && ./sbom-tool-linux-x64 generate -b /tmp/.sbom/sbom-output -bc /tmp/.sbom/'+ self.name +' -pn '+ self.name +' -pv '+ self.version +' -ps Be-Secure'
        return command

    def main(self):
        """
            generate report for scorecard, criticality_score, sbom and codeql
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
        
        elif self.report == "sbom" and self.flag:
            url = self.setup_sbom()

        if self.flag:
            data = self.fetch_report(url)
        if self.flag:
            self.write_report(data)
        self.cleanup()
        if not self.flag:
            print("[bold red] Alert! Unable to generate "
                  + self.report +
                  " report, please try again")

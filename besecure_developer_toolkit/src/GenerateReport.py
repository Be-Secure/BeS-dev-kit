import json, sys, os
from urllib.request import urlopen
from rich import print


class Report():
    def __init__(self, id:int, name: str, version: str, report: str):
        self.id = id
        self.name = name
        self.report = report
        self.version = version
        
    def fetch_report(self, url):

        if self.report == "criticality_score":
            os.system('criticality_score --repo '+url+' --format json >> /tmp/'+self.report+'.json')
            f_critical = open('/tmp/'+self.report+'.json', 'r')
            data = json.load(f_critical)
            f_critical.close()
       
        elif self.report == "codeql":
            token = os.environ['GITHUB_AUTH_TOKEN']
            cmd = 'curl -s -L -H "Accept: application/vnd.github+json" -H "Authorization: Bearer '+token+'" -H "X-GitHub-Api-Version: 2022-11-28" '+url
            os.system(cmd+' >> /tmp/'+self.report+'.json')
            codeql_f = open('/tmp/'+self.report+'.json', 'r')
            data = json.load(codeql_f)
            codeql_f.close()            
       
        else:          
            try:
                raw_data = urlopen(url)
            except Exception as e:
                exc_type, exc_obj, exc_tb = sys.exc_info()
                fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                print(exc_type, fname, exc_tb.tb_lineno)
                sys.exit(str(e))
            data = json.loads(raw_data.read())
        
        return data

    def write_report(self, data):
        
        assessment_dir = os.environ['ASSESSMENT_DIR']
        
        path = assessment_dir+'/'+self.name+'/'+self.version+'/'+self.report
        
        try:
            os.makedirs(path, exist_ok=True)
        except:
            pass
        f = open(path + '/' + self.name + '-' + self.version + '-' + self.report + '-report.json', "w")
        
        f.write(json.dumps(data, indent=4))
    
    def update_version_data(self):
        
        osspoi_dir = os.environ['OSSPOI_DIR']
        assessment_dir = os.environ['ASSESSMENT_DIR']
        report_file = open(assessment_dir+'/'+self.name+'/'+self.version+'/'+self.report+'/'+self.name + '-' + self.version + '-' + self.report + '-report.json', "r")
        version_file = open(osspoi_dir+"/version_details/"+str(self.id) + "-" + self.name + "-" "Versiondetails.json", "r+")
        
        score_data = json.load(report_file)
        if self.report == "scorecard":
            score = score_data["score"]
        elif self.report == "criticality_score":
            score = score_data["criticality_score"]
        
        version_data = json.load(version_file)
        for i in range(len(version_data)):
            if version_data[i]["version"] == self.version:
                version_data[i][self.report] = score
            else:
                pass
        version_file.seek(0)
        version_file.write(json.dumps(version_data, indent=4))
        version_file.truncate()
        report_file.close()
        version_file.close()
                
            
            
    def cleanup(self):
        if self.report == "scorecard":
            pass
        else:
            os.remove('/tmp/'+self.report+'.json')

    def main(self):
    
        if self.report == "scorecard":
            url = "https://api.securityscorecards.dev/projects/github.com/Be-Secure/"+self.name
    
        elif self.report == "criticality_score":
            if "GITHUB_AUTH_TOKEN" not in os.environ:
                print("[bold red] Alert! [green] Please use the below command to set your personal access token and try again.")
                print("[yellow]export GITHUB_AUTH_TOKEN=token")
                sys.exit()
            url = 'github.com/Be-Secure/'+self.name
                               
        elif self.report == "codeql":
            if "GITHUB_AUTH_TOKEN" not in os.environ:
                print("[bold red] Alert! [green] Please use the below command to set your personal access token and try again.")
                print("[yellow]export GITHUB_AUTH_TOKEN=token")
                sys.exit()
            url = 'https://api.github.com/repos/Be-Secure/'+ self.name +'/code-scanning/alerts?tool_name=CodeQL'
        
        data = self.fetch_report(url)
        self.write_report(data)
        self.cleanup()
        
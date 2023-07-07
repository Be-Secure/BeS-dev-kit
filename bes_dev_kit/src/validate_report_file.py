'''report-file-validate module'''
import json
import sys
import requests
from urllib.request import urlopen
from urllib.error import HTTPError
from bes_dev_kit.src.validate_version_file import VersionFileValidate
from bes_dev_kit.src.create_ossp_master import OSSPMaster
from rich import print

class ReportFileValidate():
    """Report files naming convention validation class"""

    def __init__(
            self,
            issue_id: int,
            name: str,
            namespace: str,
            branch: str
        ):
        self.issue_id = issue_id
        self.name = name
        self.namespace = namespace
        self.branch = branch
        self.report_name = ''
        self.version = ''

    def getVerionByIssueID(self, issue_id: str):
        '''retrive version tag from Be-Secure issue details'''
        url = 'https://api.github.com/repos/'\
            'Be-Secure/Be-Secure/issues/'\
            + str(issue_id)
        resp = requests.get(url,  timeout=5)
        if resp.status_code == 403:
            print(f'[red bold]Alert! [yellow]'
                    f'GitHub API rate limit '
                    f'exceeded for this system')
            sys.exit(1)
        resp = json.loads(resp.text)
        issue_version_tag = resp["body"]
        issue_version_tag = str(issue_version_tag).split("###")[1]
        issue_version_tag = issue_version_tag.strip().replace('\n', '')
        issue_version_tag = issue_version_tag.replace('\r', '')
        issue_version_tag = issue_version_tag.replace(
            'Version of the project', '')
        return issue_version_tag
    
    def getUrlResponse(self, url):
        try:
            resp = requests.get(url,  timeout=5)
        except requests.exceptions.HTTPError:
            print(f"[bold red]Alert! [yellow]HTTP"
                  f" Error: Please try again")
            sys.exit(1)
        except requests.exceptions.ReadTimeout:
            print(f"[bold red]Alert! [yellow]"
                f"Request time out: "
                f"Please check your internet "
                f"connection & try again")
            sys.exit(1)
        except requests.exceptions.ConnectionError:
            print(f"[bold red]Alert! [yellow]"
                  f"Connection error: Please try again")
            sys.exit(1)
        except requests.exceptions.RequestException:
            print(f"[bold red]Alert! [yellow]"
                  f"Exception request")
            sys.exit(1)
        if resp.text == '404: Not Found':
            return False
        else:
            return True

    def checkScorecard(self):
        '''
            check if scorecard report file exists
            for the given input
        '''
        url = 'https://raw.githubusercontent.com/'\
            + self.namespace + '/'\
            'besecure-assessment-datastore/'\
            + self.branch + '/'\
            + self.name + '/' + self.version + \
            '/scorecard/'\
            + self.name + '-' + self.version + \
            '-scorecard-report.json'
        resp = self.getUrlResponse(url)
        if resp:
            print(f'[green]{self.name}-{self.version}-'
                  'scorecard-report.json exists')
        else:
            print(f'[bold red]Alert! [green]scorecard report'
                f' not available for [yellow]{self.name},'
                f' version: {self.version}')
    
    def checkCriticality_score(self):
        '''
            check if criticality-score report file exists
            for the given input
        '''
        url = 'https://raw.githubusercontent.com/'\
            + self.namespace + '/'\
            'besecure-assessment-datastore/'\
            + self.branch + '/'\
            + self.name + '/' + self.version + \
            '/criticality_score/'\
            + self.name + '-' + self.version + \
            '-criticality_score-report.json'
        resp = self.getUrlResponse(url)
        if resp:
            print(f'[green]{self.name}-{self.version}-'
                  f'criticality_score-report.json exists')
        else:
            print(f'[bold red]Alert! [green]'
                f'criticality_score report not available'
                f' for [yellow]{self.name},'
                f' version: {self.version}')
    
    def checkCodeql(self):
        '''
            check if codeql report file exists
            for the given input
        '''
        url = 'https://raw.githubusercontent.com/'\
            + self.namespace + '/'\
            'besecure-assessment-datastore/'\
            + self.branch + '/'\
            + self.name + '/' + self.version + \
            '/sast/'\
            + self.name + '-' + self.version + \
            '-codeql-report.json'
        resp = self.getUrlResponse(url)
        if resp:
            print(f'[green]{self.name}-{self.version}-'
                  f'codeql-report.json exists')
        else:
            print(f'[bold red]Alert! [green]codeql report not '
                f'available for [yellow]{self.name},'
                f' version: {self.version}')
        
    def checkFossology(self):
        '''
            check if fossology report file exists
            for the given input
        '''
        url = 'https://raw.githubusercontent.com/'\
            + self.namespace + '/besecure-assessment-datastore/'\
            + self.branch + '/' + self.name + '/' + self.version \
            + '/license-compliance/' + self.name \
            + '-' + self.version + '-fossology-report.json'
        resp = self.getUrlResponse(url)
        if resp:
            print(f'[green]{self.name}-{self.version}-'
                  'fossology-report.json exists')
        else:
            print(f'[bold red]Alert! [green]fossology report'
                f' not available for [yellow]{self.name},'
                f' version: {self.version}')
        
    def checkSonarqube(self):
        '''
            check if sonarqube report file exists
            for the given input
        '''
        url = 'https://raw.githubusercontent.com/'\
            + self.namespace + '/'\
            'besecure-assessment-datastore/'\
            + self.branch + '/'\
            + self.name + '/' + self.version + \
            '/sast/'\
            + self.name + '-' + self.version + \
            '-sonarqube-report.json'
        resp = self.getUrlResponse(url)
        if resp:
            print(f'[green]{self.name}-{self.version}-'
                  'sonarqube-report.json exists')
        else:
            print(f'[bold red]Alert! [green]sonarqube report not '
            f'available for [yellow]{self.name},'
            f' version: {self.version}')

    def checkSbom(self):
        '''
            check if sbom report file exists
            for the given input
        '''
        url = 'https://raw.githubusercontent.com/'\
            + self.namespace + '/'\
            'besecure-assessment-datastore/'\
            + self.branch + '/'\
            + self.name + '/' + self.version + \
            '/sbom/'\
            + self.name + '-' + self.version + \
            '-sbom-report.json'
        resp = self.getUrlResponse(url)
        if resp:
            print(f'[green]{self.name}-{self.version}-'
                  'sbom-report.json exists')
        else:
            print(f'[bold red]Alert! [green]sbom report not '
                f'available for [yellow]{self.name},'
                f' version: {self.version}')
    
    def validate_report_file(self, report_name):
        '''
            This method will check if
            given report file exists
        ''' 
        self.report_name = report_name
        self.version = self.getVerionByIssueID(self.issue_id)
        if self.report_name == 'scorecard':
            self.checkScorecard()
        elif self.report_name == 'criticality_score':
            self.checkCriticality_score()
        elif self.report_name == 'codeql':
            self.checkCodeql()
        elif self.report_name == 'fossology':
            self.checkFossology()
        elif self.report_name == 'sonarqube':
            self.checkSonarqube()
        elif self.report_name == 'sbom':
            self.checkSbom()

    def check_branch_exists(self):
        """This method checks if the branch is exists
        under besecure-osspoi-datastore for given user"""
        try:
            urlopen("https://api.github.com/repos/"+self.namespace +
                    "/besecure-assessment-datastore"\
                    "/branches/"+self.branch)
        except HTTPError:
            print(f"[bold red]Alert! [green]{self.branch} does not "
                  f"exists under {self.namespace}/besecure-assessment-"
                  f"datastore")
            sys.exit()

    def check_repo_exists(self):
        """
        It checks if besecure-assessment-datastore 
        repo exists under the given user
        """
        try:
            urlopen("https://api.github.com/repos/" +
                    self.namespace
                    + "/besecure-assessment-datastore")
        except HTTPError:
            print(f"[bold red]Alert! [green]Could not find "
                  f"besecure-assessment-datastore "
                  f"under {self.namespace}")
            sys.exit()
    
    def validateIssue(self):
        obj = OSSPMaster(self.issue_id, self.name)
        obj2 = VersionFileValidate(
            self.issue_id,
            self.name,
            self.namespace,
            self.branch
        )
        if obj.check_issue_exists(self.issue_id) is False:
            print(f"[bold red]Alert! [green]Issue "
                    f"[yellow]{self.issue_id} "
                    "[green]does not exist")
            sys.exit(1)
        if obj.check_repo_exists(self.name) is False:
            print(f"[bold red]Alert! [green]Repo [yellow]"
                  f"{self.name} [green]does not exist")
            sys.exit()
        obj.check_issue_related_to_project()
        obj2.check_username()
        self.check_repo_exists()
        self.check_branch_exists()

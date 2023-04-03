import subprocess
import os
from ..osspoi.version_detail_report import osspoiVersionDetails
import json

class CodeQl():

    def __init__(self) -> None:
        pass

    def codeQl_report(self, projectName, bes_id, githubtoken, besecureAssessment):

        result = subprocess.run([
            'curl',
            '-L',
            '-H',
            "Accept: application/vnd.github+json",
            '-H',
            f"Authorization: Bearer {githubtoken}",
            '-H',
            "X-GitHub-Api-Version: 2022-11-28",
            f'https://api.github.com/repos/Be-Secure/{projectName}/code-scanning/alerts'
        ], stdout=subprocess.PIPE)
        if (result.stdout):
            result = json.loads(result.stdout)
            version = osspoiVersionDetails.getVersion(bes_id)
            codeQLPath = os.path.join(besecureAssessment, projectName, version, "sast", f"{projectName}-{version}-codeql-report.json")
            if not os.path.exists(os.path.join(besecureAssessment, projectName, version, "sast")):
                os.makedirs(os.path.join(besecureAssessment, projectName, version, "sast"))
            fileWrite = open(codeQLPath, "w+", encoding='utf-8')
            json.dump(result, fileWrite, indent=2)
            fileWrite.close()
        else:
            return f"Fail to get the codeQl report {result.stderr}"

        


codeQlReport = CodeQl()
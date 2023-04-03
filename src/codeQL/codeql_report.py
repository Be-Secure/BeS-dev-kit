import subprocess

class CodeQl():

    def __init__(self) -> None:
        pass

# curl -L   -H "Accept: application/vnd.github+json"   -H "Authorization: Bearer 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"  -H "X-GitHub-Api-Version: 2022-11-28"   https://api.github.com/repos/Be-Secure/oneTBB/code-scanning/alerts
    def codeQl_report(self, projectName, githubtoken):

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
            pass
        if result.stderr:
            pass
        # print(result.stdout)

        


codeQlReport = CodeQl()
import requests
import json

class OsspoiVersionDetails():

    def __init__(self) -> None:
        pass

    def getVersion(self, bes_id):
        try:
            loadJson = json.loads(requests.get("https://api.github.com/repos/Be-Secure/Be-Secure/issues/"+bes_id).text)
        except Exception as e:
            return f"Fails to fetch the json report for issue error: {e}"
        body_data = loadJson["body"].split("\n\n")
        for i in range(len(body_data)):
            if body_data[i] == "### Version of the project":
                return body_data[i+1]
                
        

    def osspoiVersionDetailReport(self, bes_id):
        version = self.getVersion(bes_id)
        version_detail = [{
            "version": version,
            "release_data": "",
            "criticality_score": "Not Available",
            "scorecard": "Not Available",
            "cve_details": "Not Available"
        }]

osspoiVersionDetails = OsspoiVersionDetails()
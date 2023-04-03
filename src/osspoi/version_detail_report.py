import requests
import json
import os

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

    def osspoiVersionDetailReport(self, bes_id, bes_name, besecureOsspoi):
        version = self.getVersion(bes_id)
        versionDetailPath = os.path.join(besecureOsspoi, "version_details", f"{bes_id}-{bes_name}-Versiondetails.json")
        version_detail = [{
            "version": version,
            "release_data": "",
            "criticality_score": "Not Available",
            "scorecard": "Not Available",
            "cve_details": "Not Available"
        }]
        if os.path.exists(versionDetailPath):
            fileR = open(versionDetailPath, "r+")
            fileRead = json.load(fileR)
            found = True
            for versionDetail in fileRead:
                if versionDetail["version"] == version:
                    found = False
                    break
            if found:
                fileWrite = open(versionDetailPath, "w+")
                fileRead.append(version_detail)
                json.dump(fileRead, fileWrite, indent=2)
                fileWrite.close()
        else:
            fileWrite = open(versionDetailPath, "w+")
            json.dump(version_detail, fileWrite, indent=2)
            fileWrite.close()
            

osspoiVersionDetails = OsspoiVersionDetails()
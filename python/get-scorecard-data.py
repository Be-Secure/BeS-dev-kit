import json
from urllib.request import urlopen
import sys
import os

def update_scorecard(id, name, project_version):
    
    scorecard_file = open(datastore_dir+"/"+name+"/"+project_version+"/scorecard/"+name+"-"+project_version+"-scorecard-report.json","r")
    scorecard_data = json.load(scorecard_file)
    
    score = scorecard_data["score"]
    
    version_file = open(dashboard_dir+"/bes_theme/assets/data/version_details/"+str(id)+"-"+name+"-Versiondetails.json", "r+")
    version_data = json.load(version_file)
    
    version_data[0]["scorecard"] = score
    
    version_file.seek(0)  # rewind
    json.dump(version_data, version_file, indent=4)
    version_file.truncate()
    
    scorecard_file.close()
    version_file.close()

def write_scorecard_data(id, name):
    
    try:
        raw_data = urlopen("https://api.securityscorecards.dev/projects/github.com/"+namespace+"/"+name)
    except Exception as e:
        sys.exit(str(e))
    scorecard_data = json.loads(raw_data.read())
    
    version_file = open(dashboard_dir+"/bes_theme/assets/data/version_details/"+str(id)+"-"+name+"-Versiondetails.json", "r")
    version_data = json.load(version_file)
    
    project_version = version_data[0]["version"]
    
    
    os.makedirs(datastore_dir+"/"+name+"/"+project_version+"/scorecard/", exist_ok = True)
    f = open(datastore_dir+"/"+name+"/"+project_version+"/scorecard/"+name+"-"+project_version+"-scorecard-report.json","w")    
    json.dump(scorecard_data, f, indent=4)
    f.close()
    version_file.close()
    
    update_scorecard(id, name, project_version)


    

if __name__ == "__main__":
    namespace = os.environ['GITHUB_ORG']
    id = sys.argv[1]
    name = sys.argv[2]
    dashboard_dir = os.environ['BESLIGHTHOUSE_DIR']
    datastore_dir = os.environ['DATASTORE_DIR']
    
    
    write_scorecard_data(id, name)

import json
import os
import sys
from urllib.request import urlopen

def update_criticality(id, name, project_version):
    
    criticality_file = open(datastore_dir+"/"+name+"/"+project_version+"/criticality_score/"+name+"-"+project_version+"-criticality_score-report.json","r")
    criticality_data = json.load(criticality_file)
    
    criticality_score = criticality_data["criticality_score"]
    
    version_file = open(dashboard_dir+"/bes_theme/assets/data/version_details/"+str(id)+"-"+name+"-Versiondetails.json", "r+")
    version_data = json.load(version_file)
    
    version_data[0]["criticality_score"] = criticality_score
    
    version_file.seek(0)  # rewind
    json.dump(version_data, version_file, indent=4)
    version_file.truncate()
    
    criticality_file.close()
    version_file.close()

def write_criticality_score_data(id, name):
    
    criticality_file = open(acc_root_dir+"/criticality_score.json", "r")    
    criticality_data = json.load(criticality_file)
    
    version_file = open(dashboard_dir+"/bes_theme/assets/data/version_details/"+str(id)+"-"+name+"-Versiondetails.json", "r")
    version_data = json.load(version_file)
    
    project_version = version_data[0]["version"]
    
    
    os.makedirs(datastore_dir+"/"+name+"/"+project_version+"/criticality_score/", exist_ok = True)
    f = open(datastore_dir+"/"+name+"/"+project_version+"/criticality_score/"+name+"-"+project_version+"-criticality_score-report.json","w")    
    json.dump(criticality_data, f, indent=4)
    f.close()
    version_file.close()
    
    update_criticality(id, name, project_version)


if __name__ == "__main__":
    
    id = sys.argv[1]
    name = sys.argv[2]
    acc_root_dir = os.environ['ACC_ROOT_DIR']
    dashboard_dir = os.environ['BESLIGHTHOUSE_DIR']
    datastore_dir = os.environ['DATASTORE_DIR']
    write_criticality_score_data(id, name)
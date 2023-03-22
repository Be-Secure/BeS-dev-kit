import json
import sys
import os
from urllib.request import urlopen

def write_version(bes_id, version_data):
    
    tmp_file = open(acc_root_dir+"/tmp_file", "w")
    
    raw_data = urlopen("https://api.github.com/repos/"+namespace+"/Be-Secure/issues/"+str(bes_id))

    data = json.loads(raw_data.read())
    # print(data["body"])
    body_data = iter(data["body"].splitlines())
    found = "false"
    for i in body_data:
        # if re.search("### Tech Stack", i):
        if i == "### Version of the project":
            found = "true"
            continue
        if len(i.strip()) == 0:
            continue
        if len(i.strip()) != 0 and found == "true":
            # s = str(i.split(" [")[1])
            # f.write('"bes_technology_stack": "'+ str(s.split("]")[0]) +'",\n')
            # print(i)
            tmp_file.write(i)
            version_data[0]["version"] = str(i)
            f.write(json.dumps(version_data, indent=4) +'\n')
            break


if __name__ == "__main__":
    
    namespace = os.environ['GITHUB_ORG']
    acc_root_dir = os.environ['ACC_ROOT_DIR']
    id = sys.argv[1]
    name = sys.argv[2]
    dir = os.environ['BES_OSSPOI_DIR']
    f = open(dir+"/version_details/"+str(id) + "-" + name + "-" "Versiondetails.json", "w")
    # f.write("[\n")
    # f.write("]\n")
    version_data = [{
        "version": "",
        "release_date": "",
        "criticality_score": "Not Available",
        "scorecard": "Not Available",
        "cve_details": "Not Available"
    }]
    write_version(id, version_data)
    

    
    
    
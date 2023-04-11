import sys, os, json, datetime, subprocess, shutil
from rich import print
from urllib.request import urlopen
class Version():
    def __init__(self, id: int, name: str):
        self.id = id
        self.name = name
         
    def get_version_tag(self, bes_id):      
        
        raw_data = urlopen("https://api.github.com/repos/Be-Secure/Be-Secure/issues/"+str(bes_id))
        data = json.loads(raw_data.read())
        body_data = iter(data["body"].splitlines())
        found = "false"
        for i in body_data:
            if i == "### Version of the project":
                found = "true"
                continue
            if len(i.strip()) == 0:
                continue
            if len(i.strip()) != 0 and found == "true":             
                break
        
        return str(i)
    
    def get_release_date(self, version, name):
        self.cleanup()        
        os.system('git clone -q https://github.com/Be-Secure/' + name +' /tmp/'+name)
        os.chdir('/tmp/'+name)
        proc = subprocess.Popen(['git log --tags --simplify-by-decoration --pretty="format:%ci %d" | grep -w "'+version +'"'], stdout=subprocess.PIPE, shell=True)
        (out, err) = proc.communicate()
        date = str(out).split(" ")[0]
        raw_date = date.split("'")[1]
        split_date = raw_date.split("-")
        format_datetime = datetime.datetime(int(split_date[0]), int(split_date[1]), int(split_date[2]))
        final_date = str(format_datetime.strftime("%d-%b-%Y"))    
        return final_date
    
    def cleanup(self):
        if os.path.exists(f'/tmp/{self.name}') == True:
            shutil.rmtree('/tmp/'+self.name)
  
    
    def overwrite_version_data(self, f, version_data_new, original_data, version_tag):
        for i in range(len(original_data)):
            if original_data[i]["version"] == version_tag:
                original_data[i] = version_data_new
                break
        f.seek(0)
        f.write(json.dumps(original_data, indent=4))
        f.truncate
        
    def generate_version_data(self, overwrite: bool):
        osspoi_dir = os.environ['OSSPOI_DIR']
        version_data_new = {
            "version": "",
            "release_date": "",
            "criticality_score": "Not Available",
            "scorecard": "Not Available",
            "cve_details": "Not Available"
        }
        version_tag = self.get_version_tag(self.id)
        version_data_new["version"] = version_tag
        date = self.get_release_date(version_tag, self.name)
        version_data_new["release_date"] = date
        path = osspoi_dir+"/version_details/"+str(self.id) + "-" + self.name + "-" "Versiondetails.json"
        if os.path.exists(path):
            f = open(path, "r+") 
            original_data = json.load(f)
            for i in range(len(original_data)):
                if original_data[i]["version"] == version_data_new["version"] and not overwrite:
                    write_flag = False
                    print("[bold red]Alert! [green]Version " +version_tag+ " exists")
                    break
                else:
                    write_flag = True
            if write_flag == True and not overwrite:
                original_data.append(version_data_new)
                f.seek(0)
                f.write(json.dumps(original_data, indent=4))
                f.truncate
            else:
                self.overwrite_version_data(f, version_data_new, original_data, version_tag)
        else:
            f = open(path, "w")
            f.write(json.dumps(version_data_new, indent=4))
        self.cleanup()
        f.close()
        
        
        
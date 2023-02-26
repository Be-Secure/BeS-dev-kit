import json
import sys
from urllib.request import urlopen
import datetime
import os



def write_release_date(name, tag_hash, json_data):

    raw_data = urlopen("https://api.github.com/repos/Be-Secure/"+name+"/git/tags/" + tag_hash)
    data = json.loads(raw_data.read())
    raw_date = data["tagger"]["date"]
    # print (data["tagger"]["date"])
    colon_split = str(raw_date.split(":")[0])
    T_split = str(colon_split.split("T")[0])
    hyphen_split = T_split.split("-")
    # print(hyphen_split)
    format_datetime = datetime.datetime(int(hyphen_split[0]), int(hyphen_split[1]), int(hyphen_split[2]))
    # print(str(format_datetime.strftime("%d-%b-%Y")))   
    date = str(format_datetime.strftime("%d-%b-%Y"))     
    json_data[0]["release_date"] = date
    # f.write(json.dumps(json_data))
    f.seek(0)  # rewind
    json.dump(json_data, f, indent=4)
    f.truncate()
if __name__ == "__main__":
    
    id = sys.argv[1]
    name = sys.argv[2]
    tag_hash = sys.argv[3]
    dir = os.environ['BESLIGHTHOUSE_DIR']

    # id = 343
    # name = "gramine"
    # tag_hash = "141af4d7b97091331b80bf3b63871fcba47414db"
    f = open(dir +"/bes_theme/assets/data/version_details/" + str(id) + "-" + name + "-Versiondetails.json", "r+")
    data = json.load(f)
    write_release_date(name, tag_hash, data)

    

    
    
    
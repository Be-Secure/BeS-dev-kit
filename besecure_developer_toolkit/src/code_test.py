import json
from urllib.request import urlopen
#from rich import print

json_data = json.loads(urlopen("https://raw.githubusercontent.com/pramit-d/besecure-osspoi-datastore/Koha/version_details/148-Koha-Versiondetails.json").read())
versiondetails_version_tag = json_data[0]["version"].strip()
#print(f"[value is:{versiondetails_version_tag}]")
print("version:"+versiondetails_version_tag)
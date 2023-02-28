import json
# from bs4 import BeautifulSoup
import sys
from urllib.request import urlopen
import requests
import os

def write_to_osspcve(soup, issue_id):
    maintain_table = soup.find('div', attrs={'id':'contentdiv'})
    h1 = maintain_table.find('h1')
    title_list = h1.text.split()
    product = title_list[2]
    table = soup.find('table', attrs={'class':'stats'})
    table_body = table.find('tbody')
    rows = table_body.find_all('tr')
    vuln_headers = ["No_of_Vulnerabilities", "DoS", "Code_Execution", "Overflow", "Memory_Corruption", "Sql_Injection", "XSS", "Directory_Traversal", "Http_Response_Splitting", "Bypass_something", "Gain_Information", "Gain_Privileges", "CSRF", "File_Inclusion", "No_of_exploits"]
    f = open(str(issue_id)+"-"+product+"-CVEdetails.json", "w")
    json_array=[]
    for j in range(1,len(rows)):  
        json_data = {}  
        vuln_data = rows[j].find_all('td')  
        if j == len(rows)-1 or j == len(rows)-2:
            json_data["Year"] = str(rows[j].find('th').text.strip())
        else:
            json_data["Year"] = int(rows[j].find('th').text.strip())
        for i in range(0,len(vuln_data)):
            if len(vuln_data[i].text.strip()) == 0:
                json_data[vuln_headers[i]] = ""
            elif j == len(rows)-1:
                json_data[vuln_headers[i]] = float(vuln_data[i].text.strip())
            else:
                json_data[vuln_headers[i]] = int(vuln_data[i].text.strip())
        json_array.append(json_data)
            
    f.write(json.dumps(json_array, indent=4)) 

def write_cve_data(issue_id,f):
    cve_avail = input("Enter latest cve count?(y/n)")
    cvedetails = {
        "count": 0,    
        "year": 0,                                         
        "bes_cve_details_id": "",                      
        "cvedetails_product_id": "",                      
        "cvedetails_vendor_id": ""
    }
    # TODO - Sanity check on cve url.
    # try:
    #     x = urlopen('https://www.cvedetails.com/product/'+str(product_id)+'/vendor_id='+str(vendor_id))
    #     print(x)
    # except Exception as e:
    #     print("Incorrect url https://www.cvedetails.com/product/"+ product_id +"/vendor_id="+ vendor_id)
    #     sys.exit(str(e))
    if cve_avail == "y":      
        product_id = input("Enter product id : ")
        # vendor_id = input("Enter vendor id : ") 
        source = requests.get("https://www.cvedetails.com/product/"+ product_id).text
        soup = BeautifulSoup(source, features="html5lib")
        maintain_table = soup.find('div', attrs={'id':'contentdiv'})
        h1 = maintain_table.find('h1')
        a = h1.a.get('href').split('/')
        vendor_id = a[2]
        table = soup.find('table', attrs={'class':'stats'})
        # print(table)
        table_body = table.find('tbody')
        rows = table_body.find_all('tr')
        # l = len(rows)
        # print(rows[l-3])
        cols_header = rows[len(rows)-3].find('th').text
        # print(int(cols_header))
        cols_data = rows[len(rows)-3].find('td').text
        # print(int(cols_data))
        cvedetails["count"] = int(cols_data)
        cvedetails["year"] = int(cols_header)
        cvedetails["cvedetails_product_id"] = str(product_id)
        cvedetails["cvedetails_vendor_id"] = str(vendor_id)
        write_to_osspcve(soup, issue_id)
    f.write('"cvedetails": '+ json.dumps(cvedetails, indent=4)+ ",\n")
    # print(l)
        

            
        
def check_issue_exists(id):
    try:
        x = urlopen('https://github.com/'+namespace+'/BeSLighthouse/issues/'+id)
    except Exception as e:
        print("Could not find issue with id : "+id)
        sys.exit(str(e))

def write_project_repos_data(file_pointer, project_data):
    project_repos = {
        "main_github_url": "",
        "main_bes_url": "",
        "all_projects": [                                                                        
            {
                "id": 0,
                "name": "",
                "url": ""
            }
        ],
        "all_bes_repos": [                                                                  
            {
                "id": 0,
                "name": "",
                "url": ""
            }
                    
        ]
    }
    project_repos.update({"main_github_url": project_data["parent"]["html_url"]}) 
    project_repos.update({"main_bes_url": project_data["html_url"]})
    project_repos["all_projects"][0]["id"] = project_data["parent"]["id"]     
    project_repos["all_projects"][0]["name"] = project_data["parent"]["full_name"]
    project_repos["all_projects"][0]["url"] = project_data["parent"]["html_url"]
    project_repos["all_bes_repos"][0]["id"] = project_data["id"]
    project_repos["all_bes_repos"][0]["name"] = project_data["full_name"]
    project_repos["all_bes_repos"][0]["url"] = project_data["html_url"]         
    file_pointer.write('"project_repos": '+ json.dumps(project_repos, indent=4) + ","+"\n")


def write_tags(f, bes_id):
    url = 'https://api.github.com/repos/'+namespace+'/BeSLighthouse/issues/'+str(bes_id)+'/labels'
    tags_json_data = urlopen(url)
    tags_dict = json.loads(tags_json_data.read())
    tags = []
    for i in range(len(tags_dict)):
        tags.append(tags_dict[i]["name"])
    f.write('"tags": ' + json.dumps(tags, indent=4) + "\n")


def write_tech_stack(bes_id):
    raw_data = urlopen("https://api.github.com/repos/"+namespace+"/BeSLighthouse/issues/"+str(bes_id))

    data = json.loads(raw_data.read())

    # print(data["body"])
    body_data = iter(data["body"].splitlines())
    found = "false"
    for i in body_data:
        # if re.search("### Tech Stack", i):
        if i == "### Tech Stack":
            found = "true"
            continue
        if len(i.strip()) == 0:
            continue
        if len(i.strip()) != 0 and found == "true":
            s = str(i.split(" [")[1])
            f.write('"bes_technology_stack": "'+ str(s.split("]")[0]) +'",\n')
            break

def write_languages(name):
    raw_data = urlopen("https://api.github.com/repos/"+namespace+"/"+name+"/languages")
    data = json.loads(raw_data.read())
    # languages=[]
    # for i in range(len(data)):
    #     tags.append(tags_dict[i]["name"])
    f.write('"language": ' + json.dumps(data, indent=4) + ",\n")


if __name__ == "__main__":
    
    acc_root_dir = os.environ['ACC_ROOT_DIR']
    namespace = os.environ['GITHUB_ORG']
    bes_id = sys.argv[1]
    project_name = sys.argv[2]
    check_issue_exists(bes_id)
    repo_keys = [ "bes_id", "bes_tracking_id", "issue_url", "name", "full_name", "description", "bes_technology_stack", "watchers_count", "forks_count", "stargazers_count", "size", "open_issues", "created_at", "updated_at", "pushed_at", "git_url", "clone_url", "html_url", "homepage", "owner", "project_repos", "license", "language", "tags" ]
    try:
        json_data = urlopen('https://api.github.com/repos/'+namespace+'/'+project_name)
    except Exception as e:
        print("Could not find "+ project_name +" under "+namespace)
        sys.exit(str(e))
    project_data = json.loads(json_data.read())
    f = open(acc_root_dir+"/ossp_data.json", "w")
    f.write("{\n")
    for i in repo_keys:
        # if i == "cve_details" :
        #     write_cve_data(bes_id, f)
        
        if i == "issue_url":
            f.write('"issue_url": ' + '"https://github.com/'+namespace+'/BeSLighthouse/issues/' + str(bes_id) +'",\n')
        elif i == "bes_technology_stack":
            write_tech_stack(bes_id)
        elif i == "project_repos":
            write_project_repos_data(f, project_data)
        elif i == "tags":
            write_tags(f, bes_id)
        elif i == "language":
            write_languages(project_name)
        elif i == "owner" or i == "license":
            f.write('"' + i + '": '+ json.dumps(project_data[i], indent=4) + ","+"\n")
        elif i == "bes_id":
            f.write('"id": '+ str(bes_id) + ","+"\n")      
        elif i == "bes_tracking_id":
            f.write('"' + i + '": '+ str(bes_id) + ","+"\n")
        else:
            f.write('"' + i + '": '+ json.dumps(project_data[i]) + ","+"\n")
    f.write("},\n")
    # print(f)
    f.close()
    f = open(acc_root_dir+"/ossp_data.json", "r")
    print(f.read())

    
    
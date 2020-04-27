import nmap3 
import json
import sys
from bs4 import BeautifulSoup
import requests
print("Please wait ....")
print("----------------------------------------")
nmScan = nmap3.Nmap()
result = nmScan.nmap_version_detection(sys.argv[1])
#json_re = json.loads(result)
#print(result)
SERVICES = []

for i in result:

    version = ''
    name = ''
    product = ''
    method = ''
    conf = ''
    try:
        protocal = i['protocol']
    except:
        pass
    try:
        port = i['port']
    except:
        pass
    try:
        name = i['service']['name']
    except: 
        pass
    try:
        version = i['service']['version']
    except:
        pass
    try:
        product = i['service']['product']
    except : 
        pass
    try:
        method = i['service']['method']
    except: 
        pass
    try:
        conf = i['service']['conf']
    except:
        pass
    print("Protocal : " , protocal)
    print("Port : " , port)
    print("Name : ", name)
    print("Product : " , product)
    print("Conf : " , conf)
    print("Method : " , method)
    print("Version: " , version)
    if name not in SERVICES:
        SERVICES.append(name)
    print("-------------------------------------------")


def find_endpoints():
    #TODO
    pass

def find_subdomains():
    #TODO
    pass


def rapid7_search(name):
    query = 'https://rapid7.com/db/?q='+name+'&type=metasploit'
    res = requests.get(query)
    soup = BeautifulSoup(res.content, 'html.parser')
    try:
        g_class = soup.find_all("section", class_="vulndb__results")
    #print(g_class)
        for i in g_class:
            try:
                a = i.find_all('a')
                for j in a:
                    s = j.get('href')
                    if s is not None:
                        print(s)
            except:
                pass
    except : 
        print("No exploit regarding this")

for i in SERVICES:
    if i != '':
        rapid7_search(i)
    else:
        print("No service to look for exploit")

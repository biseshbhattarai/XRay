#! /usr/bin/python3
import nmap3 
import json
import sys
from bs4 import BeautifulSoup
import requests
import urllib
from urllib.parse import urlparse




URLS = []
NAMES = []
def xray(uri):
    nmScan = nmap3.Nmap()
    result = nmScan.nmap_version_detection(uri)
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

        def rapid7_search(name):
            query = 'https://rapid7.com/db/?q='+name+'&type=metasploit'
            res = requests.get(query)
            soup = BeautifulSoup(res.content, 'html.parser')
            try:
                g_class = soup.find_all("section", class_="vulndb__results")
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
                print("No exploit regarding this", name)
    print("Looking for possible exploits...")

    for i in SERVICES:
        if i != '':
            rapid7_search(i)
        else:
            print("No service to look for exploit")



def scraper(q):
   
    query = q.replace(' ', '+')
    URL = f"https://google.com/search?q={query}"
    # desktop user-agent
    USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:65.0) Gecko/20100101 Firefox/65.0"
    # mobile user-agent
    MOBILE_USER_AGENT = "Mozilla/5.0 (Linux; Android 7.0; SM-G930V Build/NRD90M) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.125 Mobile Safari/537.36"
    headers = {"user-agent" : USER_AGENT}
    resp = requests.get(URL, headers=headers)    
    results = []
    soup = BeautifulSoup(resp.content, "html.parser")
    for g in soup.find_all('div', class_='r'):
        anchors = g.find_all('a')
        if anchors:
            link = anchors[0]['href']
            title = g.find('h3').text
            item = {
            "title": title,
            "link": link
            }
            results.append(item)
    for i in results : 
        s = i['link']
        nam = i['title']
        o = urlparse(s)
        p = o.netloc
        URLS.append(p)
        NAMES.append(nam)

                                      
 
   
def run():
    print("""
 \\ / /     //   ) )                  
  \  /     //___/ /   ___             
  / /     / ___ (   //   ) ) //   / / 
 / /\\   //   | |  //   / / ((___/ /  
/ /  \\ //    | | ((___( (      / /   
AUTHOR : Bishesh@xpl0iter 
""")
    in_q = input("Enter website or related query : ")
    print("Scrap exact or all related website : (1/2)")
    s = int(input(" => :"))
    if s == 2:
        scraper(in_q)
        print("Urls Scraped : ")
        print(URLS)
        print("This gonna take some time grab a coffee , ☕")
        for u in URLS:
            print("Now XRaying .. ", u)
            xray(u)
    elif s == 1:
        print("Now XRaying .. ", in_q)
        xray(in_q)

if __name__ == '__main__':
    run()
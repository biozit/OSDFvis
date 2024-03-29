import geoip2.webservice
import re
import socket
import os
from xml.dom import minidom
from urllib.request import urlopen
from bs4 import BeautifulSoup 
import requests
import traceback
import time
from radar import RadarClient
import unidecode

class location:
  
  def __init__(self, city, country):
     self.city = city
     self.county = country

fCaches = open('caches.txt')
fOrigin = open('origins.txt')

dic = {}
user = ""
key = ""
dict = {}
bs_data = BeautifulSoup(requests.get("https://topology.opensciencegrid.org/rgsummary/xml").content, 'xml') 
radar = RadarClient("")
total = 0;
ok = 0;
fail = 0;

osgstorage = open('/home/fandri/geoIPcache/config-repo/etc/cvmfs/osgstorage-auth.conf', 'r');
osgstorageidomain = open('/home/fandri/geoIPcache/config-repo/etc/cvmfs/domain.d/osgstorage.org.conf', 'r');
osgstoragelines = osgstorage.readlines()
osgstoragelinesd = osgstorageidomain.readlines()



with geoip2.webservice.Client(user, key) as client:
  
  rg = bs_data.find_all('ResourceGroup') 
  for alld in rg:
    try:
      resiAll = alld.find_all("Resource")
    except:
      resiAll = alld.find("Resource")
      print('a')
    for res in resiAll:
      try:
        active =  (str(res.find("Active")))
        cache = res.find("Services").find("Name")
        if(str(cache) == "<Name>XRootD cache server</Name>" and active == "<Active>true</Active>"):
            total = total + 1;
            FQDN = str(res.find("FQDN")).replace("<FQDN>","").replace("</FQDN>","").strip() 
            name = str(res.find("Name")).replace("<Name>","").replace("</Name>","").strip() 
            city = str(alld.find('Site').find('City')).strip();
            country = str(alld.find('Site').find('Country')).strip();
            ipCache = socket.gethostbyname(str(FQDN).replace("<FQDN>","").replace("</FQDN>","").strip())
            city = unidecode.unidecode(str(city).replace("<City>","").replace("</City>","").strip())
            country = str(country).replace("<Country>","").replace("</Country>","").strip() 

            response = client.city(ipCache)
            citygeo = unidecode.unidecode(str(response.city.name))

            countrygeo = str(response.country.name)
            count = 0;
            for row in osgstoragelines:
              count = count + len(re.findall(FQDN,row,re.IGNORECASE));

            if(count == 1):
              okosgstorage = "OK"
            elif(count == 0):
              okosgstorage = "nop"
            else:
              okosgstorage = "DUP"

            count = 0;

            for row in osgstoragelinesd:
              count = count + len(re.findall(FQDN,row,re.IGNORECASE))
            
            if(count == 1):
              okosgstoraged = "OK"
            elif(count == 0):
              okosgstoraged = "nop"
            else:
              okosgstoraged = "DUP"
              
            print("\n"+FQDN+";", end="")
            print(name+";", end="")

            if(city == citygeo and country == countrygeo):
              dict[FQDN] = 1;
              print(" ------ok------ " , end="")
              ok = ok + 1
            else:
              dict[FQDN] = 0;
              print("------PROBLEM------", end="")
              print(city + " GeoIP Maxim -----> " + citygeo, end="")
              print(country + " GeoIPMaxim ----->" + countrygeo,end="")
              fail = fail + 1;
      except Exception as exc:
        print(exc)

lstCache = fCaches.readlines()
lstOrigin = fOrigin.readlines()

print("-----------------")
for caches in lstCache:
  try: 
    print(caches.strip(),end=';');
    if caches in dict:
      if dict[caches] == 1:
        print("ok")
      else:
        print("problem")
  
  except Exception as exc:
    print("problem caches position" + caches.trim());

  try:
    r = requests.get('https://'+caches.strip()+':8443', timeout=15)
    
    if 'Server' in r.headers:
      print(r.headers['Server'])
    else:
      print('none')

  except Exception as exc:
    try:
      r = requests.get('https://'+caches.strip()+':8000', timeout=15)
    
      if 'Server' in r.headers:
        print(r.headers['Server'])
      else:
        print('none')
    except Exception as exc:
      print("problem cache version" + caches.strip());


print("-----------------")
for caches in lstOrigin:
    print(caches.strip(),end=';');

    try:
      r = requests.get('https://'+caches.strip()+':1094', timeout=15)
    
      if 'Server' in r.headers:
        print(r.headers['Server'])
      else:
        print('none')

    except Exception as exc:

      try:
        r = requests.get('https://'+caches.strip()+':1095', timeout=15)
      
        if 'Server' in r.headers:
          print(r.headers['Server'])
        else:
          print('none')
      except Exception as exc:
        print("problem cache version" + caches.strip());




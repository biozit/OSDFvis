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

f = open('caches.txt')
dic = {}
user = "838862"
key = "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"
dict = {}
bs_data = BeautifulSoup(requests.get("https://topology.opensciencegrid.org/rgsummary/xml").content, 'xml') 
radar = RadarClient("prj_test_pk_c278f3d47a7d7f9c8931beb44e48fb5f00d15dfb")
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
              print(" ------ok------ " , end="")
              ok = ok + 1
            else:
              print("------PROBLEM------", end="")
              print(city + " GeoIP Maxim -----> " + citygeo, end="")
              print(country + " GeoIPMaxim ----->" + countrygeo,end="")
              fail = fail + 1;

            #print("CONT " + response.continent.name,end="")
            #print(" osgstorage: " + okosgstorage,end="");
            #print(" osgstoraged: " + okosgstoraged,end="");
      except Exception as exc:
        traceback.print_exception(exc)

print("caches: "+ str(total) +" ok " + str(ok) + " Fail "+ str(fail));

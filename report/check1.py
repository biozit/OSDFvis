import geoip2.webservice
import socket
import os
from xml.dom import minidom
from urllib.request import urlopen
from bs4 import BeautifulSoup 
import requests
import traceback
import time
from radar import RadarClient

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
            FQDN = res.find("FQDN")
            print(FQDN)
            city = str(alld.find('Site').find('City'));
            country = str(alld.find('Site').find('Country'));
            ipCache = socket.gethostbyname(str(FQDN).replace("<FQDN>","").replace("</FQDN>","").strip())
  
            city = str(city).replace("<City>","").replace("</City>","").strip() 
            country = str(country).replace("<Country>","").replace("</Country>","").strip() 

            response = client.city(ipCache)
            citygeo = str(response.city.name)
            response = client.country(ipCache)
            countrygeo = str(response.country.name)


            radarpos = radar.geocode.ip(ip=ipCache)
            print(radarpos.city)

            print(city + " GeoIP Maxim -----> " + citygeo +  "| GeoIP radar -----> "+ radarpos.city)
            print(country + " GeoIPMaxim ----->" + countrygeo + "| GeoIP radar ----->" + radarpos.country)

            if(city == citygeo and country == countrygeo and city == radarpos.city and radarpos.country):
              print("------ok------")
            else:
              print("------PROBLEM------")
            time.sleep(1)
      except Exception as exc:
        traceback.print_exception(exc)

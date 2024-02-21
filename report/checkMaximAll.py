import geoip2.webservice
import re
import h3
import socket
import csv
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
filer =  open('hostsgeoip.csv', 'w', newline='')
writer = csv.writer(filer)
writer.writerow(["IP","Type","Hostname", "City", "Country", "CityGeopIP", "CountryGeoIP","LatGeo","LongGeop","LatTop","LongTop","Distance(km)"])

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
        cache = str(res.find("Services").find("Name")).strip().replace("<Name>","").replace("</Name>","")
        #if(active == "<Active>true</Active>") and (str(cache) == "XRootD cache server"):
        if(active == "<Active>true</Active>") and (str(cache) == "XRootD cache server"):
            total = total + 1;
            FQDN = str(res.find("FQDN")).replace("<FQDN>","").replace("</FQDN>","").strip() 

            latt = str(alld.find('Site').find('Latitude')).strip().replace("<Latitude>","").replace("</Latitude>","").strip();
            logt = str(alld.find('Site').find('Longitude')).strip().replace("<Longitude>","").replace("</Longitude>","").strip();
            city = str(alld.find('Site').find('City')).strip().replace("<City>","").replace("</City>","").strip();
            country = str(alld.find('Site').find('Country')).strip().replace("<Country>","").replace("</Country>","").strip();


            ipCache = "NO"
            try:
                fqdn = str(FQDN).replace("<FQDN>","").replace("</FQDN>","").strip()
                ipCache = socket.gethostbyname(fqdn)
                city = unidecode.unidecode(str(city).replace("<City>","").replace("</City>","").strip())
                country = str(country).replace("<Country>","").replace("</Country>","").strip() 

                response = client.city(ipCache)
                citygeo = unidecode.unidecode(str(response.city.name))
                countrygeo = str(response.country.name)


                print("\n\n"+FQDN, end="")
                if(city == citygeo and country == countrygeo):
                    print(" ------ok------ " , end="")
                    ok = ok + 1
                else:
                    geoipLat = float(response.location.latitude)  
                    geoipLong = float(response.location.longitude)
                    print(geoipLat) 
                    print(geoipLong) 
                    print(latt) 
                    print(logt) 
                    coords_1 = (geoipLat,geoipLong)
                    coords_2 = (float(latt),float(logt))

                    distance = h3.point_dist(coords_1, coords_2, unit='km')
                    print(distance);
                    writer.writerow([ipCache,cache,fqdn,city,country,citygeo,countrygeo,geoipLat,geoipLong,latt,logt,distance])
                    print("------PROBLEM------", end="")
                    print(city + " GeoIP Maxim -----> " + citygeo, end="")
                    print(country + " GeoIPMaxim ----->" + countrygeo,end="")
                    print(country + " GeoIPMaxim ----->" + countrygeo,end="")
                    
                    fail = fail + 1;
            except Exception as exc:
                print(exc)

      except Exception as exc:
        print(exc)
filer.close()
print("caches: "+ str(total) +" ok " + str(ok) + " Fail "+ str(fail));

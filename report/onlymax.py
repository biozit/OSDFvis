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

f = open('nrp.txt')
dic = {}
user = "838862"
key = "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"
dict = {}
total = 0;
ok = 0;
fail = 0;
rg = f.readlines()

with geoip2.webservice.Client(user, key) as client:
  
  for ipCache in rg:
    ipCache = ipCache.strip();
    response = client.city(ipCache)
    citygeo = unidecode.unidecode(str(response.city.name))
    countrygeo = str(response.country.name)
    print(ipCache);
    print(citygeo);
    print(countrygeo);
    print("--------------------------")


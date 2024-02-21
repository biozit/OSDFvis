import geoip2.webservice
import socket
import os
from xml.dom import minidom
from urllib.request import urlopen

f = open('caches.txt')

user = "838862"
key = "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"

for line in f:
#  with geoip2.webservice.Client(user, key) as client:
    line = line.rstrip();
    ipCache = socket.gethostbyname(line)
    print(ipCache)
     
#    response = client.city(ipCache)
#    print(response.city.name)
#    print(response.country.name)
    #root = urlopen('https://topology.opensciencegrid.org/rgsummary/xml')
    root = minidom.parse("top.xml")
    #rg = file1.getElementsByTagName('TOPIC');
    #print(rg)
    #for elem in rg:
    #  print(elem.attributes.values())
    for demand in root.getElementsByTagName('ResourceGroup'):
      for tp in demand.getElementsByTagName('Facility'):
        print(tp.getAttribute("id"))

#    for demand in root.getElementsByTagName('ResourceGroup'):
#        print(demand.getAttribute("GridType"))


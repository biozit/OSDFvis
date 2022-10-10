#!/usr/bin/python3
import subprocess
import os
import traceback
from time import sleep, perf_counter
from threading import Thread
from subprocess import PIPE 
import time
from XRootD import client
import numpy as np
from influxdb import InfluxDBClient
from datetime import datetime
from pythonping import ping

file_lorigins = open("/opt/OSDFvis/origins.txt", "r")
lorigins = lines = file_lorigins.read().splitlines()
db_pass = open("/opt/pass", "r")

URL="graph.t2.ucsd.edu"
password=db_pass.readline().strip()
user="cachemon"
db="cachemon_db"


key = 'CACHE_FQDN'
cache = 'NONONONO'
for line in open("/etc/xrootd-environment", 'r'):
    if(line.find('CACHE_FQDN') != -1):
        t1 = line.split(" ");
        cache = t1[1].split("=")[1]


clientflux = InfluxDBClient(URL, 8086, user, password, db)
def xrdcpy(origin,n,timeout):
        process = client.CopyProcess()

        sf = origin.split(' ')
        server = sf[0]
        filet = "/"+sf[1]
        print(server)
        print(filet)
        myclient = client.FileSystem(server)
        status = myclient.copy(server+filet,'/xcache/t'+str(n), force=True)
        print(status)

def checkSize(ftt,timeout):
     seconds = time.time()
     run = True
     sleep(2)
     while(run == True):
             try:
                    path = tmppath+"t"+str(ftt);   
                    if(os.path.exists(path)):   
                           file_size = os.path.getsize(path)
                           dr[ftt] = file_size
                    end = time.time()
                    el = end - seconds;
                    sleep(1)
                    if(el > timeout):
                           run = False
             except Exception as e:
                    print(e)
                    traceback.print_exc()
            

tests = 1
threads = []
threadsTimer = []
dr = np.empty(tests)
timeout = 10;
tmppath = "/xcache/"



for origin in lorigins:
        try: 
                hosto = origin.split(" ")[0]
                hosto = hosto.split("//")[1]
                hosto = hosto.split(":")[0]

                dataping = ping(hosto, count=10)
                for d in dataping:
                    print(d.time_elapsed)
 
                json_body = [  
                    {  
                        "measurement": "heatmaplt",  
                        "tags": {  
                            "origin": oradd+"|"+cache  
                        },  
                        "time": datetime.utcnow().isoformat() + "Z",
                        "fields": {  
                            "duration": str(media) 
                        }  
                    },  
                ]
                clientflux.write_points(json_body)

                oradd = origin.split(" ")[0]
                for n in range(0, tests):
                       if(os.path.exists(tmppath+"t"+str(n))):
                              os.remove(tmppath+"/t"+str(n))
                       t = Thread(target=xrdcpy, args=(origin,n,2))
                       threads.append(t)
                       t.start()
                       t = Thread(target=checkSize, args=(n,timeout))
                       threadsTimer.append(t)
                       t.start()

                for x in threadsTimer:
                       x.join()
                print("join timer")
                for x in threads:
                       x.join()
                print("join copy")
                media = 0
                for n in dr:
                       print(n)
                       media = media + n;

                media = media / len(dr)

                media = media/timeout

                print("MEDIA___________"+str(media))
                
                json_body = [  
                    {  
                        "measurement": "heatmappar",  
                        "tags": {  
                            "origin": oradd+"|"+cache  
                        },  
                        "time": datetime.utcnow().isoformat() + "Z",
                        "fields": {  
                            "duration": str(media) 
                        }  
                    },  
                ]
                clientflux.write_points(json_body)
           
                for n in range(0, tests):
                       if(os.path.exists(tmppath+"t"+str(n))):
                              os.remove(tmppath+"t"+str(n))
                
               
 
        except Exception as e:
                print(e)
                traceback.print_exc()


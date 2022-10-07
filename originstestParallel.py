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


file_lorigins = open("/opt/OSDFvis/origins.txt", "r")
lorigins = lines = file_lorigins.read().splitlines()
db_pass = open("/opt/pass", "r")

URL="http://graph.t2.ucsd.edu:8086"
password=db_pass.readline().strip()
user="cachemon"
db="cachemon_db"

key = 'CACHE_FQDN'
for line in open("/etc/xrootd-environment", 'r'):
    if(line.find('CACHE_FQDN') == True):
        t1 = line.split(" ");
        cache = t1[1].split("=")[1]

print(cache)
cache = os.getenv(key)


def executeCommandBD(com, typer):

        with open('outooo.txt','w+') as fout:
                with open('errooo.txt','w+') as ferr:
                        out=subprocess.call([com],stdout=fout,stderr=ferr,timeout=500,shell=True)
                        fout.seek(0)
                        output=fout.read()
                        ferr.seek(0)
                        errors = ferr.read()
                        if(typer == 1):
                               return errors
                        else:
                               return output
def getSpeed(datoutput, prot):
        size = 0
        time = 0
        try:   
               if(prot == 1):

                      for l in datoutput.splitlines():
                            if(l.find("Length") != -1):
                                  size = float(l.split(" ")[1])
                            if(l.find("100%") != -1):
                                   time = float(l.split("=")[1].replace("s",""))
                      resp = size/time
                      print(resp)
                      return resp
               else:
                      datoutput = datoutput.split("]")
                      speed = datoutput[len(datoutput)-2]
                      if(speed.find("MB") != -1):
                            m = 1048576
                      else:
                            m = 1024
                      speed = speed.replace("[","");
                      speed = speed.replace("M","");
                      speed = speed.replace("k","");
                      speed = speed.replace("B","");
                      speed = speed.replace("/","");
                      speed = speed.replace("s","");
                      speed = float(speed) * m
                      print(speed)
                      return speed

        except Exception as e:
               traceback.print_exc()
               return "timeout"


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
                    #print(el) 
                    #print("file" +str(ftt)+ " "+ str(el)+" size "+str(file_size))
                    if(el > timeout):
                           run = False
             except Exception as e:
                    print(e)
                    traceback.print_exc()
            

tests = 5
threads = []
threadsTimer = []
dr = np.empty(tests)
timeout = 10;
tmppath = "/xcache/"

for origin in lorigins:
        try: 
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
                
                dbc = "curl --user " +user+":"+password+ " -XPOST " + URL+"/write?db="+db+" --data-binary 'heatmappar,origin="+oradd+"|"+cache+" value="+str(media)+"'";
                print(dbc)
                executeCommandBD(dbc,1);
                print(dbc)
                for n in range(0, tests):
                       if(os.path.exists(tmppath+"t"+str(n))):
                              os.remove(tmppath+"t"+str(n))
 
        except Exception as e:
                dbc = "curl --user " +user+":"+password+ " -XPOST " + URL+"/write?db="+db+" --data-binary 'heatmappar,origin="+oradd+"|"+cache+" value=-100'";
                executeCommandBD(dbc,1);
                print(e)
                traceback.print_exc()


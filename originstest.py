#!/usr/bin/python3
import subprocess
import os
import traceback

file_lorigins = open("/opt/origins.txt", "r")
lorigins = lines = file_lorigins.read().splitlines()

URL="http://graph.t2.ucsd.edu:8086"
password=""
user="cachemon"
db="cachemon_db"

key = 'CACHE_FQDN'
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
                
def getLatency(datoutput):
        try:
                for l in datoutput.splitlines():
                        if(l.find("rtt") != -1):
                               timeavg = l.split("/")[4]
                               print(timeavg)
                               return timeavg
        except Exception as e:
                traceback.print_exc()
                return "timeout" 

for origin in lorigins:
        try:
                print(origin)
                oradd = origin.split(" ")[0]
                if(origin[0] == 'h'):
                      path = origin.replace(" ","")
                      dd = "wget -O /dev/null --report-speed=bits " +path
                      ex = executeCommandBD(dd,1)
                      resp = getSpeed(ex,1)
                else:
                      path = origin.split(" ")
                      path = path[0] + "/" + path[1]
                      dd = "/opt/xrdcopy -f " +path + " ." 
                      ex = executeCommandBD(dd,1)
                      resp = getSpeed(ex,2)
                dbc = " "
                dbc = "curl --user " +user+":"+password+ " -XPOST " + URL+"/write?db="+db+" --data-binary 'heatmap,origin="+oradd+"|"+cache+" value="+str(resp)+"'";
        except Exception as e:
                dbc = "curl --user " +user+":"+password+ " -XPOST " + URL+"/write?db="+db+" --data-binary 'heatmap,origin="+oradd+"|"+cache+" value=-100'";
                executeCommandBD(dbc,1);
                print(e)
                traceback.print_exc()

        try:
                executeCommandBD(dbc,2);
                ioradd = oradd
                oradd = origin.split(" ")[0]
                oradd = oradd.split("//")[1]
                oradd = oradd.split(":")[0]
                cc = "ping -c 4 "+oradd
                ex = executeCommandBD(cc,2)
                resp = getLatency(ex)
                dbc = "curl --user " +user+":"+password+ " -XPOST " + URL+"/write?db="+db+" --data-binary 'heatmaplt,origin="+ioradd+"|"+cache+" value="+str(resp)+"'";
                executeCommandBD(dbc,1);
        except Exception as e:
                dbc = "curl --user " +user+":"+password+ " -XPOST " + URL+"/write?db="+db+" --data-binary 'heatmaplt,origin="+ioradd+"|"+cache+" value=-100'";
                executeCommandBD(dbc,1);
                print(e)
                traceback.print_exc()


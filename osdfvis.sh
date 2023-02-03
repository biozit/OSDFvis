#!/bin/bash
FILE=/usr/bin/git
if [ ! -f "$FILE" ]; then
    echo "45 * * * * root bash /opt/OSDFvis/cleanTest.sh;" > /etc/cron.d/clean.cron
    yum -y install git >>/var/log/vis 2>&1
    yum -y install xrootd-tcp-stats >>/var/log/vis 2>&1
    echo "xrd.tcpmonlib ++ /usr/lib64/libXrdTCPStats.so" >> /etc/xrootd/config.d/40-stash-cache-plugin.cfg 
    pip3 install numpy >>/var/log/vis 2>&1
    pip3 install pythonping >>/var/log/vis 2>&1
    pip3 install influxdb>>/var/log/vis 2>&1
    cd /opt >>/var/log/vis 2>&1
    /usr/bin/git clone https://github.com/biozit/OSDFvis.git >>/var/log/vis 2>&1
    cd /usr/lib64
    rm /usr/lib64/libXrdAccSciTokens-5.so
    wget https://s3-west.nrp-nautilus.io/dweitzel/xrootd-scitokens/libXrdAccSciTokens-5.so
    supervisorctl restart stash-cache
    supervisorctl restart stash-cache-auth
fi

cd /opt/OSDFvis >>/var/log/vis 2>&1
/usr/bin/python3 /opt/OSDFvis/originstestParallel.py >>/var/log/vis 2>&1

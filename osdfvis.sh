#!/bin/bash
FILE=/usr/bin/git
if [ ! -f "$FILE" ]; then
    yum -y install git >>/var/log/vis 2>&1
    pip3 install numpy >>/var/log/vis 2>&1
    pip3 install pythonping >>/var/log/vis 2>&1
    cd /opt >>/var/log/vis 2>&1
    /usr/bin/git clone https://github.com/biozit/OSDFvis.git >>/var/log/vis 2>&1
fi

cd /opt/OSDFvis >>/var/log/vis 2>&1
/usr/bin/python3 /opt/OSDFvis/originstestParallel.py >>/var/log/vis 2>&1
/usr/bin/python3 /opt/OSDFvis/originstest.py >>/var/log/vis 2>&1

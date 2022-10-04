#!/bin/bash
FILE=/usr/bin/git
if [ ! -f "$FILE" ]; then
    yum -y install git
    pip3 install numpy
fi

cd /opt
git clone https://github.com/biozit/OSDFvis.git
cd OSDFvis
python3 originstestParallel.py
python3 originstest.py


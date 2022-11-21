#!/bin/bash
source /etc/xrootd-environment
if [ -d "/xcache/osgconnect/public/fandri/cacheTest" ] 
then
    cd /xcache/osgconnect/public/fandri/cacheTest
    data=`readlink /xcache/osgconnect/public/fandri/cacheTest/*`
    rm -f $data
    rm -f /xcache/osgconnect/public/fandri/cacheTest/*
    echo "cleaning"
fi


if [ -d "/xcache/user/ligo/test_access" ] 
then
    cd /xcache/user/ligo/test_access
    data=`readlink /xcache/user/ligo/test_access/*`
    rm -f $data
    rm -f /xcache/user/ligo/test_access/*
    echo "cleaning"
fi


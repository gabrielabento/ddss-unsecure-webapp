#!/bin/bash
# 
# MSI DDSS 2020/2021 - Assignment 2
# The code and resources available in this repository are to be used in the scope of the DDSS course.
#
# Authors: Nuno Antunes <nmsa@dei.uc.pt>, João Antunes <jcfa@dei.uc.pt>
#



#
# ATTENTION: This will stop and delete all the running containers
# Comment out if you are using docker for other ativities
#
docker rm $(docker stop $(docker ps -a -q)) 

mkdir -p python/app/logs


# add  -d  to the command below if you want the containers running in background without logs
docker-compose  -f docker-compose-python-psql.yml up --build
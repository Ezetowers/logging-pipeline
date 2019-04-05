#!/bin/bash

cd ./src/publishLogs
docker build -t publish-logs .

cd ../retrieveLogs
docker build -t retrieve-logs .

cd ../..
docker-compose up

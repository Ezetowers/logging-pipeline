#!/bin/bash

cd ./src/api/publishLogs
docker build -t publish-logs . --no-cache

cd ../retrieveLogs
docker build -t retrieve-logs . --no-cache

cd ../..
docker build -t db-server -f db/Dockerfile . --no-cache

cd ../
docker-compose up

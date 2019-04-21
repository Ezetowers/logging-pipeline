#!/bin/bash

cd ./src

docker build -t publish-logs -f api/publish-logs/Dockerfile .
docker build -t retrieve-logs -f api/retrieve-logs/Dockerfile .
docker build -t db-server -f db/Dockerfile . 

cd ../
docker-compose up

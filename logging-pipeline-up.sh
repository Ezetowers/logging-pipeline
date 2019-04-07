#!/bin/bash

cd ./src

docker build -t publish-logs -f api/publish-logs . --no-cache
docker build -t retrieve-logs -f api/retrieve-logs . --no-cache
docker build -t db-server -f db/Dockerfile . --no-cache

cd ../
docker-compose up

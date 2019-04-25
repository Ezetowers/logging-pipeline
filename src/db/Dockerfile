FROM python:3.7-alpine
COPY ./ /src
WORKDIR /src/db
ENTRYPOINT exec python3 -u db_server.py

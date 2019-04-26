FROM python:3.7-alpine
COPY ./ /src
WORKDIR /src/api/publish-logs
ENTRYPOINT exec python3 -u post_handler.py

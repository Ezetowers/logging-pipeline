FROM python:3.7-alpine
RUN pip3 install requests; pip3 install flask
COPY ./ /src
WORKDIR /src/api/retrieve-logs
ENTRYPOINT python3 -u get_handler.py

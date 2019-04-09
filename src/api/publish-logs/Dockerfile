FROM python:3.7-alpine
RUN pip3 install requests; pip3 install flask
COPY ./ /src
WORKDIR /src/api/publish-logs
CMD ["python3", "-u", "post_handler.py"]

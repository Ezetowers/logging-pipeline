FROM python:3.7-alpine
RUN pip3 install requests; pip3 install flask
COPY post_handler.py .
CMD ["python3", "post_handler.py"]

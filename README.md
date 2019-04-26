# logging-pipeline

Repository for the 1st project of "Sistemas Distribuidos I". It features a distributed logging pipeline that can be used by a REST API.

## Installation

Just download the repo and you are good to go! Docker and docker-compose required.

## Usage

The logging pipeline can be started by using the following comand in the root dir of this repository.

``` bash
sh logging-pipeline-up.sh
```

### Publish logs

Publishing new log entries is done by connecting to a TCP socket in ``localhost:6060`` with a message 'POS', the size of the JSON body and a JSON body in the form of:
  
```json
{
  "msg" : "your message here",
  "timestamp" : "YYYY-MM-DD HH:MM:SS.SSSSSS",
  "tags" : "tag1 tag2",
}
```

### Retrieve logs

To retrieve logs entries you have to connect to a TCP socket in ``localhost:6070`` with message 'GET', the size of the JSON body and a JSON body with optional request params in the form of:
 
* from: a timestamp in the form ``YYYY-MM-DD HH:MM:SS.SSSSSS``
* to: a timestamp in the form ``YYYY-MM-DD HH:MM:SS.SSSSSS``
* tags: one tag
* pattern: an string pattern appearing in the message.

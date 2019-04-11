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

Publishing new log entries is done by doing a POST request to ``localhost:6060/log/<appId>``. The JSON body must be in the form of:
  
```json
{
  "msg" : "your message here",
  "timestamp" : "YYYY-MM-DD HH:MM:SS.SSSSSS",
  "tags" : "tag1 tag2",
}
```

### Retrieve logs

To retrieve logs entries you have to do a GET request to ``localhost:6060/log/<appId>``. The following query params are accepted:
 
* from: a timestamp in the form ``YYYY-MM-DD HH:MM:SS.SSSSSS``
* to: a timestamp in the form ``YYYY-MM-DD HH:MM:SS.SSSSSS``
* tags: one tag
* pattern: an string pattern appearing in the message.

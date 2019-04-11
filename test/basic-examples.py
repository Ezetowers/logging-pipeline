import requests

r = requests.get("http://localhost:6070/log/001")

print("-----------------------------Empiezo el testing-------------------------------------")

print("GET 001: Recibi {} logs, con status {}".format(len(r.json().get('logs')), r.status_code))

logs = [{"msg" : "primer log", "tags" : "error", "timestamp" : "2019-02-01 09:30:20.120000"},
 {"msg" : "segundo log", "tags" : "error", "timestamp" : "2019-02-02 15:00:20.120000"},
 {"msg" : "tercer log", "tags" : "info", "timestamp" : "2010-02-01 12:45:20.120000"},
 {"msg" : "cuarto log", "tags" : "info", "timestamp" : "2008-02-01 21:05:20.120000"},
 {"msg" : "quinto log, relacionado con el segundo", "tags" : "info healthcheck", "timestamp" : "2019-02-01 09:35:20.120000"}]

print("")
print("")
print("----------------------------Cargo varios logs----------------------------------------")

#for log in logs:
    #r = requests.post("http://localhost:6060/log/001", json=log)
    #print("POST 001: envie {} y recibi {} con status {}".format(log, r.json(), r.status_code))

print("")
print("")
print("---------------------------Hago requests sobre la base cargada----------------------")

r = requests.get("http://localhost:6070/log/001")
print("GET 001: Recibi {} logs, con status {}".format(len(r.json().get('logs')), r.status_code))
print("")
r = requests.get("http://localhost:6070/log/002")
print("GET 002: Recibi {} logs, con status {}".format(len(r.json().get('logs')), r.status_code))
print("")

print("")
print("-----------------Requests sobre tags-----------------------")

r = requests.get("http://localhost:6070/log/001?tags=error")
print("GET 001 para tags error: Recibi {} logs, con status {}".format(len(r.json().get('logs')), r.status_code))
print("Recibi los logs {}".format([log.get('msg') for log in r.json().get('logs')]))
print("")

r = requests.get("http://localhost:6070/log/001?tags=info")
print("GET 001 para tags info: Recibi {} logs, con status {}".format(len(r.json().get('logs')), r.status_code))
print("Recibi los logs {}".format([log.get('msg') for log in r.json().get('logs')]))
print("")

r = requests.get("http://localhost:6070/log/001?tags=healthcheck")
print("GET 001 para tags healthcheck: Recibi {} logs, con status {}".format(len(r.json().get('logs')), r.status_code))
print("Recibi los logs {}".format([log.get('msg') for log in r.json().get('logs')]))
print("")

print("")
print("-----------------Requests sobre patterns-----------------------")

r = requests.get("http://localhost:6070/log/001?pattern=log")
print("GET 001 para pattern log: Recibi {} logs, con status {}".format(len(r.json().get('logs')), r.status_code))
print("Recibi los logs {}".format([log.get('msg') for log in r.json().get('logs')]))
print("")

r = requests.get("http://localhost:6070/log/001?pattern=primer")
print("GET 001 para pattern primer: Recibi {} logs, con status {}".format(len(r.json().get('logs')), r.status_code))
print("Recibi los logs {}".format([log.get('msg') for log in r.json().get('logs')]))
print("")

r = requests.get("http://localhost:6070/log/001?pattern=segundo")
print("GET 001 para pattern segundo: Recibi {} logs, con status {}".format(len(r.json().get('logs')), r.status_code))
print("Recibi los logs {}".format([log.get('msg') for log in r.json().get('logs')]))
print("")

print("")
print("------------------Requests para timestamps-------------------")

r = requests.get("http://localhost:6070/log/001?from=2008-02-01+21:05:20.120000")
print("GET 001 para timestamp from 2008-02-01 21:05:20.120000: Recibi {} logs, con status {}".format(len(r.json().get('logs')), r.status_code))
print("Recibi los logs {}".format([log.get('msg') for log in r.json().get('logs')]))
print("")

r = requests.get("http://localhost:6070/log/001?from=2019-02-01+09:35:20.120000")
print("GET 001 para timestamp from 2019-02-01 09:35:20.120000: Recibi {} logs, con status {}".format(len(r.json().get('logs')), r.status_code))
print("Recibi los logs {}".format([log.get('msg') for log in r.json().get('logs')]))
print("")

r = requests.get("http://localhost:6070/log/001?to=2019-02-02+15:00:20.120000")
print("GET 001 para timestamp to 2019-02-02 15:00:20.120000: Recibi {} logs, con status {}".format(len(r.json().get('logs')), r.status_code))
print("Recibi los logs {}".format([log.get('msg') for log in r.json().get('logs')]))
print("")

r = requests.get("http://localhost:6070/log/001?to=2010-02-01+12:45:20.120000")
print("GET 001 para timestamp to 2010-02-01 12:45:20.120000: Recibi {} logs, con status {}".format(len(r.json().get('logs')), r.status_code))
print("Recibi los logs {}".format([log.get('msg') for log in r.json().get('logs')]))
print("")

print("")
print("-------------------Requests mixtos-----------------------------")

r = requests.get("http://localhost:6070/log/001?from=2010-02-01+12:45:20.120000&to=2019-02-01+09:35:20.120000")
print("GET 001 para timestamp from 2010-02-01 12:45:20.120000 y to 2019-02-01 09:35:20.120000: Recibi {} logs, con status {}".format(len(r.json().get('logs')), r.status_code))
print("Recibi los logs {}".format([log.get('msg') for log in r.json().get('logs')]))
print("")

r = requests.get("http://localhost:6070/log/001?pattern=segundo&tags=info")
print("GET 001 para pattern segundo y tags info: Recibi {} logs, con status {}".format(len(r.json().get('logs')), r.status_code))
print("Recibi los logs {}".format([log.get('msg') for log in r.json().get('logs')]))
print("")

import datetime
import requests
from requests_threads import AsyncSession

session = AsyncSession(n=100)

async def gets_to_log001():
    for _ in range(100):
        await session.get("http://localhost:6070/log/001")
    r = requests.get("http://localhost:6070/log/001")
    print("GET 001: Recibi {} logs, con status {}".format(len(r.json().get('logs')), r.status_code))

async def populate_log():
    for i in range(100):
        current_time = datetime.datetime.now()
        timestamp = str(current_time)
        await session.post("http://localhost:6060/log/001",
        json={"msg" : "log number "+str(i), "tags" : "load-test", "timestamp" : timestamp})
    r = requests.get("http://localhost:6070/log/001")
    print("GET 001: Recibi {} logs, con status {}".format(len(r.json().get('logs')), r.status_code))

if __name__ == '__main__':
    session.run(gets_to_log001)
    session.run(populate_log)

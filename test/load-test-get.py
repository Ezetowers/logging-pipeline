import datetime
import requests
import random
import time
from requests_threads import AsyncSession

session = AsyncSession(n=100)

async def gets_to_log001():
    for i in range(100):
        time.sleep(2)
        start = datetime.datetime.now()
        appId = str(random.randrange(0, 999)).zfill(3)
        await session.get("http://localhost:6070/log/"+appId+"?pattern=log")
        delta = (datetime.datetime.now() - start).total_seconds()
        print("Iteracion {}, tarde {}".format(i, delta))
    r = requests.get("http://localhost:6070/log/001")
    print("GET 001: Recibi {} logs, con status {}".format(len(r.json().get('logs')), r.status_code))

if __name__ == '__main__':
    session.run(gets_to_log001)

import asyncio
from config import Config
from sql import PGSQL
from sql import SQLite
from sql import generate_uuid

#from utils import DBTransactionExecuteSync
from utils.tasks import PGR_after
from utils import CleanLocalDB
from utils.tasks import CleanLocalDB_after

import time

#print(Config().PostgreSQL("host"))

loop = asyncio.get_event_loop()

uuid = generate_uuid()

#loop.run_until_complete(CleanLocalDB_after(24*60))
loop.run_until_complete(CleanLocalDB_after(5))
#loop.run_until_complete(CleanLocalDB())

#loop.run_until_complete(PGR_after(5))
#loop.run_until_complete(PGR_after(10))
#print(Config().get("bus_number"))

#loop.run_until_complete(PGSQL().addAllCNT((2, 9, 7), "E777", time.strftime("%d.%m.%Y | %H:%M:%S")))
#loop.run_until_complete(SQLite().addAllCNT((15, 20, 5), time.strftime("%d.%m.%Y | %H:%M:%S")))

#loop.run_until_complete(PGSQL().addUUID(uuid))
#loop.run_until_complete(PGSQL(uuid=uuid).setPeopleCount_up(16))
#loop.run_until_complete(PGSQL(uuid=uuid).setPeopleCount_down(16))
#loop.run_until_complete(PGSQL(uuid=uuid).setPeopleCount(0))


#loop.run_until_complete(SQLite().createTable("local"))
#loop.run_until_complete(SQLite().addUUID(uuid))
#loop.run_until_complete(SQLite(uuid=uuid).setPeopleCount(15))
#loop.run_until_complete(SQLite(uuid=uuid).setTime(time.strftime("%d.%m.%Y | %H:%M:%S")))


#loop.run_until_complete(PGSQL().createTable("PCDB"))
#loop.run_until_complete(PGSQL().addAllCNT(7, "E777", time.strftime("%d.%m.%Y | %H:%M:%S")))
#loop.run_until_complete(PGSQL(uuid=uuid).addAllCNT(7, "E777", time.strftime("%d.%m.%Y | %H:%M:%S")))
"""
#loop.run_until_complete(PGSQL().createTable("PCDB"))
loop.run_until_complete(PGSQL().addUUID(uuid))
loop.run_until_complete(PGSQL(uuid=uuid).setPeopleCount(10))
loop.run_until_complete(PGSQL(uuid=uuid).setBusNumber("E777"))
loop.run_until_complete(PGSQL(uuid=uuid).setTime(time.strftime("%d.%m.%Y | %H:%M:%S")))
#loop.run_until_complete(PGSQL(uuid="8601fed3-14ef-4dec-bb5f-7e22b6bc7636").setPeopleCount(10))
"""

#loop.run_until_complete(PGSQL().addUUID(generate_uuid()))
#loop.run_until_complete(PGSQL(uuid=generate_uuid()).createTable("PCDB"))
#loop.run_until_complete(PGSQL(uuid="777").createTable("PCDB"))
#loop.run_until_complete(PGSQL().setPeopleCount(10))
#loop.run_until_complete(PGSQL().setBusNumber("E777"))
import asyncio
import asyncpg
import aiosqlite
from config import Config
import time

_host = Config().PostgreSQL("host")
_port = Config().PostgreSQL("port")
_user = Config().PostgreSQL("user")
_password = Config().PostgreSQL("password")

_table = Config().PostgreSQL("table")

_bus_num = "777777t"

async def __DBTransactionExecuteSync(request):
	try:
		connection = await asyncpg.connect(host=_host, port=_port, user=_user, password=_password)
		async with connection.transaction():
			await connection.execute(f"""
				INSERT INTO {_table} (
				uuid,
				bus_number,
				count,
				count_up,
				count_down,
				time
				)
				VALUES
				{request}
				ON CONFLICT DO NOTHING;
									 """)

	except Exception as e:
		print(e)

	finally:
		#print("[DEBUG] Close connection")
		await connection.close()

async def __GetLocalData():
	try:
		request = ""
		async with aiosqlite.connect(Config().SQLite("db")) as db:
			cursor = await db.execute(f"""SELECT * FROM {Config().SQLite("table")}""")
			async for row in cursor:
				#print(row)
				request += f"""('{row[0]}', '{_bus_num}', {row[1]}, {row[2]}, {row[3]}, '{row[4]}'),\n"""


			#print(request[:-2])
			await db.commit()
			#await db.close()

			return request[:-2].replace("None", "0")

	except Exception as e:
		print(e)

async def PGR(time_):
	while True:
		time.sleep(time_)
		
		request = await __GetLocalData()
		#print(request)
		await __DBTransactionExecuteSync(request)
		print("[INFO] Local sqlite3 db sync with remote PostgreSQL")


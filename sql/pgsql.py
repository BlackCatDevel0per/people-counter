import asyncio
import asyncpg

from . import generate_uuid

from config import Config

class PGSQL:

	def __init__(self, table=None, uuid=None):
		self._host = Config().PostgreSQL("host")
		self._port = Config().PostgreSQL("port")
		self._user = Config().PostgreSQL("user")
		self._password = Config().PostgreSQL("password")

		self._table = table
		if self._table == None:
			self._table = Config().PostgreSQL("table")

		_uuidarg = uuid
		if _uuidarg == None:
			self._current_uuid = generate_uuid.generate()
		elif _uuidarg != None:
			self._current_uuid = str(uuid)
		else:
			print("uuid get error")

	async def createTable(self, name: str):
		try:
			#print(f"[INFO] UUID: {self._current_uuid}") # OK!
			#if self._table != None:
			#	return False
			connection = await asyncpg.connect(host=self._host, port=self._port, user=self._user, password=self._password)
			async with connection.transaction():
				await connection.execute(f"""CREATE TABLE {name} \
										   (\
										   uuid VARCHAR(38) PRIMARY KEY, \
										   bus_number VARCHAR(32),\
										   count INTEGER, \
										   time VARCHAR(32) \
										   );""")
				print(f"[INFO] Table \"{name}\" created successfully!")
		except asyncpg.exceptions.DuplicateTableError:
			print(f"[INFO] Table \"{name}\" exists!")

		except Exception as e:
			print(f"[WARNING] Create table \"{name}\" error!\n{e}")
##############################
	async def addUUID(self, uuid: str):
		try:
			connection = await asyncpg.connect(host=self._host, port=self._port, user=self._user, password=self._password)
			async with connection.transaction():
				await connection.execute(f"""INSERT INTO "{self._table}" \
										     (uuid) VALUES ('{uuid}');\
										  """)
				print(f"[INFO] UUID: \"{uuid}\" added to db successfully!")

		except Exception as e:
			print(f"[WARNING] Add UUID \"{uuid}\" error!\n{e}")
###
	async def setPeopleCount(self, count: int):
		try:
			connection = await asyncpg.connect(host=self._host, port=self._port, user=self._user, password=self._password)
			async with connection.transaction():
				await connection.execute(f"""UPDATE "{self._table}" \
											 SET count = {count} \
											 WHERE uuid = '{self._current_uuid}';
										  """)
				print(f"[INFO] People count \"{count}\"->\"{self._current_uuid}\" added to db successfully!")

		except Exception as e:
			print(f"[WARNING] Add people count \"{count}\"->\"{self._current_uuid}\" error!\n{e}")
###
	async def setBusNumber(self, number: str):
		try:
			connection = await asyncpg.connect(host=self._host, port=self._port, user=self._user, password=self._password)
			async with connection.transaction():
				await connection.execute(f"""UPDATE "{self._table}" \
										   	 SET bus_number = '{number}' \
										   	 WHERE uuid = '{self._current_uuid}';
										  """)
				print(f"[INFO] Bus number \"{number}\"->\"{self._current_uuid}\" added to db successfully!")

		except Exception as e:
			print(f"[WARNING] Add bus number \"{number}\"->\"{self._current_uuid}\" error!\n{e}")
###
	async def setTime(self, time: str):
		try:
			connection = await asyncpg.connect(host=self._host, port=self._port, user=self._user, password=self._password)
			async with connection.transaction():
				await connection.execute(f"""UPDATE "{self._table}" \
										   	 SET time = '{time}' \
										   	 WHERE uuid = '{self._current_uuid}';
										  """)
				print(f"[INFO] Time \"{time}\"->\"{self._current_uuid}\" added to db successfully!")

		except Exception as e:
			print(f"[WARNING] Add btime \"{time}\"->\"{self._current_uuid}\" error!\n{e}")
##############################

	async def addAllCNT(self, count: int, number: str, time: str):
		try:
			await self.addUUID(self._current_uuid)
			await self.setPeopleCount(count)
			await self.setBusNumber(number)
			await self.setTime(time)
			print("[INFO] DONE!")
		except Exception as e:
			print(f"[FAIL!] Add count, bus_number, time \"{count, number, time}\"->\"{self._current_uuid}\" failed!\n{e}")

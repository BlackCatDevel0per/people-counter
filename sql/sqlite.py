import aiosqlite

from . import generate_uuid
from config import Config

class SQLite:
	def __init__(self, uuid=None, table=None):
		self._table = table
		if self._table == None:
			self._table = Config().SQLite("table")

		_uuidarg = uuid
		if _uuidarg != False:
			if _uuidarg == None:
				self._current_uuid = generate_uuid.generate()
				#print("[INFO] Generated new uuid!") ???
			elif _uuidarg != None:
				self._current_uuid = str(uuid)
			else:
				print("uuid get error")


	async def __DBExecute(self, request: str, debug: str = None, exception_text: str = None, EXTYPE: type = Exception):
		try:
			async with aiosqlite.connect(Config().SQLite("db")) as db:
				await db.execute(request)
				await db.commit()
				if debug != None: print(debug)
				
				#print("[DEBUG] Close db")
				#await db.close()

		#except sqlite3.OperationalError as e:
		#	print(e)

		except EXTYPE as e:
			print(e)
			if exception_text != None: print(exception_text)


	async def createTable(self, name: str):
		# No bus number
		await self.__DBExecute(f"""CREATE TABLE {name} 
											  (
											  uuid VARCHAR(38) PRIMARY KEY, 
											  count INTEGER, 
											  count_up INTEGER, 
											  count_down INTEGER, 
											  time VARCHAR(32) 
											  );""",
											  f"[INFO] Table \"{name}\" created successfully!",
											  f"[WARNING] Create table \"{name}\" error!")

	async def addUUID(self, uuid: str):
		await self.__DBExecute(f"""INSERT INTO "{self._table}" 
								   (uuid) VALUES ('{uuid}');
								""",
		f"[INFO] UUID: \"{uuid}\" added to db successfully!",
		f"[WARNING] Add UUID \"{uuid}\" error!")

	async def setPeopleCount(self, count: int):
		await self.__DBExecute(f"""UPDATE "{self._table}" 
								   SET count = {count} 
								   WHERE uuid = '{self._current_uuid}';
								""",
	   f"[INFO] People count \"{count}\"->\"{self._current_uuid}\" added to db successfully!",
	   f"[WARNING] Add people count \"{count}\"->\"{self._current_uuid}\" error!")

	async def setPeopleCount_up(self, count: int):
		await self.__DBExecute(f"""UPDATE "{self._table}" 
								   SET count_up = {count} 
								   WHERE uuid = '{self._current_uuid}';
								""",
	   f"[INFO] People count (UP) \"{count}\"->\"{self._current_uuid}\" added to db successfully!",
	   f"[WARNING] Add people count \"{count}\"->\"{self._current_uuid}\" error!")

	async def setPeopleCount_down(self, count: int):
		await self.__DBExecute(f"""UPDATE "{self._table}" 
								   SET count_down = {count} 
								   WHERE uuid = '{self._current_uuid}';
								""",
	   f"[INFO] People count (DOWN) \"{count}\"->\"{self._current_uuid}\" added to db successfully!",
	   f"[WARNING] Add people count \"{count}\"->\"{self._current_uuid}\" error!")

	async def setTime(self, time: str):
		await self.__DBExecute(f"""UPDATE "{self._table}" 
								   SET time = '{time}' 
								   WHERE uuid = '{self._current_uuid}';
							    """, 
	   f"[INFO] Time \"{time}\"->\"{self._current_uuid}\" added to db successfully!", 
	   f"[WARNING] Add btime \"{time}\"->\"{self._current_uuid}\" error!")


	async def ___addAllCNT(self, count: tuple = None, time: str = None): ###########
		try:
			assert len(count) == 3, "Кортеж count должен состоять из 3 значений!"

			cdown, cup, call = count
			
			Auuid = 					f"""INSERT INTO "{self._table}" 
								     		  (uuid) VALUES ('{self._current_uuid}');
								  	 	"""
			
			Acall = 					f"""UPDATE "{self._table}" 
											  SET count = {call} 
									    	  WHERE uuid = '{self._current_uuid}';
									 	"""
			
			Acup = 					f"""UPDATE "{self._table}" 
											  SET count_up = {cup} 
											  WHERE uuid = '{self._current_uuid}';
										"""
			
			Acdown = 					f"""UPDATE "{self._table}"
											  SET count_down = {cdown} 
											  WHERE uuid = '{self._current_uuid}';
										"""
			
			Atime = 					f"""UPDATE "{self._table}" 
									   		  SET time = '{time}' 
									   		  WHERE uuid = '{self._current_uuid}';
									 	"""

			await self.__DBExecute(f"{Auuid}\n {Acall}\n {Acup}\n {Acdown}\n {Atime}".replace("None", "0"))

			"""
			await self.addUUID(self._current_uuid)
			await self.setPeopleCount(call)
			await self.setPeopleCount_up(cup)
			await self.setPeopleCount_down(cdown)
			await self.setTime(time)
			"""

			print("[INFO] AllCNT SQLite3 DONE!")
		except Exception as e:
			print(f"[FAIL!] Add count, bus_number, time \"{count, time}\"->\"{self._current_uuid}\" to local db failed!\n{e}")

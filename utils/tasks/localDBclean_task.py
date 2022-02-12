import asyncio
import time

from .. import CleanLocalDB

async def CleanLocalDB_after(timer: int):
	while True:
		time.sleep(timer)
		
		try:
			await CleanLocalDB()
			print("[INFO] Local sqlite3 db cleaned!")
		except Exception as e:
			print(e)


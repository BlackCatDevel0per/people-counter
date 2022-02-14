import asyncio

from .. import CleanLocalDB

async def CleanLocalDB_after(timer: int):
	while True:
		try:
			await CleanLocalDB()
			await asyncio.sleep(timer)
			print("[INFO] Local sqlite3 db cleaned!")
		except Exception as e:
			print(e)


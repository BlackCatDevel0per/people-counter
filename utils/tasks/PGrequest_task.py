import asyncio
import time

from .. import GetLocalData, DBTransactionExecuteSync

async def PGR_after(timer: int):
	while True:
		time.sleep(timer)
		
		try:
			request = await GetLocalData()
			#print(request)
			await DBTransactionExecuteSync(request)
			print("[INFO] Local sqlite3 db sync with remote PostgreSQL")
		except Exception as e:
			print(e)


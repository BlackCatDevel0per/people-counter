import asyncio

from .. import GetLocalData, DBTransactionExecuteSync

async def PGR_after(timer: int):
	while True:
		
		try:
			await asyncio.sleep(timer)
			request = await GetLocalData()
			assert request != "", "[DEBUG] Local db is clear, no data to request"
			await DBTransactionExecuteSync(request)
			#print(request)
			print("[INFO] Local sqlite3 db sync with remote PostgreSQL")
		except Exception as e:
			print(e)


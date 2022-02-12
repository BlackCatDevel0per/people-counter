import asyncio
import aiosqlite

from config import Config

async def CleanLocalDB():
	try:
		async with aiosqlite.connect(Config().SQLite("db")) as db:
			await db.execute(f"""DELETE FROM {Config().SQLite("table")}""")
			await db.commit()
			
			#print("[DEBUG] Close db")
			#await db.close()

	#except sqlite3.OperationalError as e:
	#	print(e)

	except Exception as e:
		print(e)

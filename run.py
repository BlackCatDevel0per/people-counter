import cv2
import asyncio
from PeopleCounter import App

from utils import tasks

#asyncio.run(tasks.CleanLocalDB_after())
#asyncio.run(tasks.PGR_after(10*60))



stream = cv2.VideoCapture('Test Files/TestVedeo2.mp4')
asyncio.run(App(stream).Counter())
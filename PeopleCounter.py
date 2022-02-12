##from picamera.array import PiRGBArray
##from picamera import PiCamera
import cv2

# Изменение настроек не применяются во время работы программы (требуется перезапуск)

# Источник видео
#stream = cv2.VideoCapture(0)

# stream = cv2.VideoCapture("http://192.168.1.104:4747/video") # DroidCamX
#stream = cv2.VideoCapture('Test Files/TestVideo.avi')
stream = cv2.VideoCapture('Test Files/TestVedeo2.mp4')

from nonloopvars import persons, pid, max_p_age
from nonloopvars import current_uuid
from nonloopvars import log
from frames import vidops
from frames import binarize
from frames import detect
from frames import InfoDraw

# Импорт переменных счётчиков
from nonloopvars import cnt_up, cnt_down
from nonloopvars import prev_frame_time, new_frame_time

from nonloopvars import line_down, line_up
print("Red line y:", str(line_down))
print("Blue line y:", str(line_up))

from sql import SQLite
import time

import asyncio

import utils

class App:

	def __init__(self):
		self.persons = persons
		self.pid = pid
		self.max_p_age = max_p_age
		self.current_uuid = current_uuid
		self.log = log
		self.cnt_up = cnt_up
		self.cnt_down = cnt_down
		self.prev_frame_time = prev_frame_time
		self.new_frame_time = new_frame_time
		#self.line_down = line_down
		self.line_up = line_up

	async def Counter(self):

		while stream.isOpened():
			# for image in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
			# Чтение кадра из источника видео stream
			grabbed, frame = stream.read()
			if not grabbed:
				break
			#frame = image.array

			frame = vidops(frame)

			for i in self.persons:  # Слежение выхода за кадр каждого объекта за кадр
				i.age_one()

			# Преобразование в бинарный формат для удаления теней
			#frame, mask, mask2 = binarize(frame, grabbed)
			try:
				# Преобразование в бинарный формат для удаления теней
				frame, mask, mask2 = binarize(frame, grabbed)
			except Exception as e:
				print('EOF') ###
				print('ВЫШЛО:', self.cnt_up)
				print('ЗАШЛО:', self.cnt_down)
				print(e)
				break

			# Возвращает в переменные is_up, is_down True, если объект пересёк линию
			frame, is_up, is_down = detect(frame, mask2, self.persons, self.pid, self.max_p_age)
			if is_up:
				# Add how many outsided bus
				self.cnt_up += 1
				await SQLite().addUUID(self.current_uuid)
				await SQLite(uuid=self.current_uuid).setPeopleCount_up(self.cnt_up)
				await SQLite(uuid=self.current_uuid).setTime(time.strftime("%d.%m.%Y | %H:%M:%S"))
			elif is_down:
				# Add how many insided bus
				self.cnt_down += 1
				await SQLite().addUUID(self.current_uuid)
				await SQLite(uuid=self.current_uuid).setPeopleCount_down(self.cnt_down)
				await SQLite(uuid=self.current_uuid).setTime(time.strftime("%d.%m.%Y | %H:%M:%S"))

			# Рисование линий счётчика (на его работу не влияет)
			frame = InfoDraw.lines(frame)
			# Рисование счётчиков UP и DOWN
			frame = InfoDraw.count(frame, self.cnt_up, self.cnt_down)
			# Переменные для работы счётчика fps
			self.new_frame_time, self.prev_frame_time = InfoDraw.fps(
				frame, (self.prev_frame_time, self.new_frame_time))

			# Вывод кадров
			cv2.imshow('Stream', frame)
			#cv2.imshow('Mask', mask)

			if cv2.waitKey(1) & 0xFF == ord('q'):  # Завершение цикла на 'q'
				break

		await SQLite(uuid=self.current_uuid).setPeopleCount(self.cnt_down - self.cnt_up) # Add data after loop break

		###############
		#   Очистка   #
		###############
		self.log.flush()
		self.log.close()

		stream.release()
		cv2.destroyAllWindows()

asyncio.run(App().Counter())
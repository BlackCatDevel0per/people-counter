##from picamera.array import PiRGBArray
##from picamera import PiCamera
import cv2

# Изменение настроек не применяются во время работы программы (требуется перезапуск)

from nonloopvars import persons, pid, max_p_age
from nonloopvars import current_uuid, new_current_uuid
#from nonloopvars import log
from frames import vidops
from frames import binarize
from frames import detect
from frames import InfoDraw
from frames import SleepMotion

# Импорт переменных счётчиков
from nonloopvars import cnt_up, cnt_down, cnt_all
from nonloopvars import prev_frame_time, new_frame_time

from nonloopvars import sleep_time_minutes, sleep_motion_sensitivity
from nonloopvars import mdt, sleep_enable

from nonloopvars import line_down, line_up

from sql import SQLite
import time

import asyncio

import utils

import schedule

class App:

	def __init__(self, stream):
		self.stream = stream
		self.persons = persons
		self.pid = pid
		self.max_p_age = max_p_age
		self.current_uuid = current_uuid
		self.new_current_uuid = new_current_uuid
		#self.log = log
		self.cnt_up = cnt_up
		self.cnt_down = cnt_down
		self.cnt_all = cnt_all # count inside bus
		self.prev_frame_time = prev_frame_time
		self.new_frame_time = new_frame_time
		#self.line_down = line_down
		self.line_up = line_up

		self.counting = True
		self._mdt = 0

		self.sleep_motion_sensitivity = sleep_motion_sensitivity
		self.mdt = mdt
		#self.sleep_enable = sleep_enable
		sleep_time = sleep_time_minutes

		print("Red line y:", str(line_down))
		print("Blue line y:", str(line_up))
		
		if sleep_enable and sleep_time != 0:
			print("[INFO COUNTER] Sleep mode enabled!")
			#sleep_time = 0
			#schedule.every(sleep_time).seconds.do(self.CSETF)
			schedule.every(sleep_time).minutes.do(self.CSETF)

		# SM
		###
		frame1 = self.stream.read()[1]
		frame1 = vidops(frame1)
		#frame1 = vidops(frame1, True)
		gray1 = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)
		gray1 = cv2.GaussianBlur(gray1, (21, 21), 0)
		self.gray1 = gray1
		#cv2.imshow('window',frame1)

		###

		#self.skip_frame_count = 5 # starts from than frame number
		#self.stream.set(cv2.CAP_PROP_POS_FRAMES, self.skip_frame_count) # set skip frame

	def CSETF(self):
		if self.cnt_up == 0 and self.cnt_down == 0 and self.cnt_all == 0:
			self.counting = False
			print("[INFO COUNTER] Sleep...")

	def zero_count(self, all_0: bool=True):
		# Function for reset all counts & generate new uuid
		if all_0:
			self.cnt_up = 0
			self.cnt_down = 0
			self.cnt_all = 0
			self.current_uuid = self.new_current_uuid()
		#print(self.current_uuid)
		#print(self.new_current_uuid())

	async def Counter(self):

		while self.stream.isOpened():
			# for image in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
			# Чтение кадра из источника видео self.stream
			grabbed, frame = self.stream.read()
			if not grabbed:
				break
			#frame = image.array

			frame = vidops(frame)
			#frame = vidops(frame, True)

			# Sleep Process for saveing cpu resources (only motion detection)
			schedule.run_pending()
			if not self.counting: # var..
				# Soon
				cv2.putText(frame, "SLEEP", (10, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2, cv2.LINE_AA)
				if SleepMotion(frame, self.gray1, self.sleep_motion_sensitivity): # sens: 200 OK!
					self._mdt += 1
					print(self._mdt)

					if self._mdt == self.mdt: # After 5 detections
						print("[INFO COUNTER] Wake up!")
						self._mdt = 0
						self.counting = True

				continue
			##


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

				self.cnt_all -= 1
				await SQLite(uuid=self.current_uuid).setPeopleCount(self.cnt_all) # Add data after loop break

			elif is_down:
				# Add how many insided bus
				self.cnt_down += 1
				await SQLite().addUUID(self.current_uuid)
				await SQLite(uuid=self.current_uuid).setPeopleCount_down(self.cnt_down)
				await SQLite(uuid=self.current_uuid).setTime(time.strftime("%d.%m.%Y | %H:%M:%S"))

				self.cnt_all += 1
				await SQLite(uuid=self.current_uuid).setPeopleCount(self.cnt_all) # Add data after loop break


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

		#if not self.stream.isOpened() and self.counting == False:
		#	return False

		#await SQLite(uuid=self.current_uuid).setPeopleCount(self.cnt_down - self.cnt_up) # Add data after loop break

		###############
		#   Очистка   #
		###############
		#self.log.flush()
		#self.log.close()

		self.stream.release()
		cv2.destroyAllWindows()

# Источник видео
#stream = cv2.VideoCapture(0)

#stream = cv2.VideoCapture("http://192.168.1.104:4747/video") # DroidCamX
#stream = cv2.VideoCapture('Test Files/TestVideo.avi')
#stream = cv2.VideoCapture('Test Files/TestVedeo2.mp4')

#asyncio.run(App(stream).Counter())
#asyncio.run(App().Counter_console())
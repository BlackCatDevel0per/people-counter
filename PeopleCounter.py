##from picamera.array import PiRGBArray
##from picamera import PiCamera
import numpy as np
import cv2
import imutils
from config import Config
import time

# Изменение настроек не применяются во время работы программы

# Object Options
obj_number_font_size = Config().get("obj_number_font_size")

# Источник видео
#stream = cv2.VideoCapture(0)

#stream = cv2.VideoCapture("http://192.168.1.104:4747/video") # DroidCamX
#stream = cv2.VideoCapture('Test Files/TestVideo.avi')
stream = cv2.VideoCapture('Test Files/TestVedeo2.mp4')

from vars import persons, pid, max_p_count
from vars import pts_L1, pts_L2, pts_L3, pts_L4
from vars import line_down_color, line_up_color
from vars import line_down_bcolor, line_up_bcolor
from vars import font
from vars import log
from vid import vidops
from vid import binarize
from vid import contours

cnt_up = 0
cnt_down = 0

# fps
prev_frame_time = 0
new_frame_time = 0

while stream.isOpened():
##for image in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
	# Чтение кадра из источника видео stream
	grabbed, frame = stream.read()
	if not grabbed:
		break
	#frame = image.array

	frame = vidops(frame)

	for i in persons:
		i.count_one() # Слежение выхода за кадр каждого человека за кадр


	# Преобразование в бинарный формат для удаления теней
	frame, mask, mask2 = binarize(frame, grabbed)
	"""
	try:
	except Exception as e:
		print(e)
		print('EOF') ###
		print('ВЫШЛО:', cnt_up)
		print ('ЗАШЛО:', cnt_down)
		break
	"""

	frame, is_up, is_down = contours(frame, mask2, persons, pid, max_p_count)
	if is_up:
		cnt_up += 1
	elif is_down:
		cnt_down += 1
			
	#########################
	#    Рисование пути     #
	#########################
	for i in persons:
##        if len(i.getTracks()) >= 2:
##            pts = np.array(i.getTracks(), np.int32)
##            pts = pts.reshape((-1, 1, 2))
##            frame = cv2.polylines(frame, [pts], False, i.getRGB())
##        if i.getId() == 9:
##            print str(i.getX()), ',', str(i.getY())
		cv2.putText(frame, str(i.getId()), (i.getX(), i.getY()), 
					font, obj_number_font_size, i.getRGB(), 1, cv2.LINE_AA)
		
	##########################
	#   Действия с кадрами   #
	##########################
	frame = cv2.polylines(frame, [pts_L1], False, line_down_color, thickness=2)
	frame = cv2.polylines(frame, [pts_L2], False, line_up_color, thickness=2)
	frame = cv2.polylines(frame, [pts_L3], False, line_down_bcolor, thickness=1)
	frame = cv2.polylines(frame, [pts_L4], False, line_up_bcolor, thickness=1)
	str_up = 'UP: '+ str(cnt_up)
	str_down = 'DOWN: '+ str(cnt_down)
	cv2.putText(frame, str_up, (10, 40), font, 0.5, (255, 255, 255), 2, cv2.LINE_AA)
	cv2.putText(frame, str_up, (10, 40), font, 0.5, (0, 0, 255), 1, cv2.LINE_AA)
	cv2.putText(frame, str_down, (10, 90), font, 0.5, (255, 255, 255), 2, cv2.LINE_AA)
	cv2.putText(frame, str_down, (10, 90), font, 0.5, (255, 0, 0), 1, cv2.LINE_AA)
	# display realtime fps
	new_frame_time = time.time()
	fps = 1/(new_frame_time - prev_frame_time)
	prev_frame_time = new_frame_time

	fps = str(int(fps))
	cv2.putText(frame, f"FPS: {fps}", (220, 25), font, 0.5, (255, 255, 255), 2, cv2.LINE_AA)
	cv2.putText(frame, f"FPS: {fps}", (220, 25), font, 0.5, (0, 0, 255), 1, cv2.LINE_AA)
	###########################

	cv2.imshow('Stream', frame)
	#cv2.imshow('Mask', mask)    
	

	if cv2.waitKey(1) & 0xFF == ord('q'): # Завершение цикла на 'q'
			break
	
###############
#   Очистка   #
###############
log.flush()
log.close()

stream.release()
cv2.destroyAllWindows()

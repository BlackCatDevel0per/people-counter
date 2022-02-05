##from picamera.array import PiRGBArray
##from picamera import PiCamera
import numpy as np
import cv2
import imutils
import Person
from config import Config
import time

# Изменение настроек не применяются во время работы программы

# Video Options
#rotate_degree = 90
#resize = 1.6 # for cam 2 for video 3
resize = Config().get("resize")
rotate_degree = Config().get("rotation")

# Object Options
rectangle_color = Config().get("rectangle_color")
rectangle_thickness = Config().get("rectangle_thickness")

try:
	log = open('log.txt',"w")
except:
	print("Не удалось открыть лог")

# Переменные с счетчиками входа и выхода
cnt_up   = 0
cnt_down = 0

# Источник видео
#stream = cv2.VideoCapture(0)

#stream = cv2.VideoCapture("http://192.168.1.104:4747/video") # DroidCamX
#stream = cv2.VideoCapture('Test Files/TestVideo.avi')
stream = cv2.VideoCapture('Test Files/TestVedeo2.mp4')

# Size properties
##stream.set(3,160) #Width
##stream.set(4,120) #Height

# fps
prev_frame_time = 0
new_frame_time = 0

# Raspberry Pi properties
#camera = PiCamera()
##camera.resolution = (160,120)
##camera.framerate = 5
##rawCapture = PiRGBArray(camera, size=(160,120))
##time.sleep(0.1)


# Печать свойств захвата в консоль
#for i in range(19):
#	print(i, stream.get(i))

# Отступ линий по высоте и ширине (лучше оставить по умолчанию 480, 640)
#h = 480
#w = 640
h, w = Config().get("lines_pos")
frameArea = h*w
areaTH = frameArea/250
#print('Area Threshold', areaTH)

# Линии входа/выхода
line_up = int(2*(h/5))
line_down = int(3*(h/5))

up_limit = int(1*(h/5))
down_limit = int(4*(h/5))

print("Red line y:", str(line_down))
print("Blue line y:", str(line_up))
#line_down_color = (255,0,0)
#line_up_color = (0,0,255)
line_down_color = Config().get("line_down_color")
line_up_color = Config().get("line_up_color")
pt1 = [0, line_down]
pt2 = [w, line_down]
pts_L1 = np.array([pt1,pt2], np.int32)
pts_L1 = pts_L1.reshape((-1,1,2))
pt3 = [0, line_up]
pt4 = [w, line_up]
pts_L2 = np.array([pt3,pt4], np.int32)
pts_L2 = pts_L2.reshape((-1,1,2))

pt5 = [0, up_limit]
pt6 = [w, up_limit]
pts_L3 = np.array([pt5,pt6], np.int32)
pts_L3 = pts_L3.reshape((-1,1,2))
pt7 = [0, down_limit]
pt8 = [w, down_limit]
pts_L4 = np.array([pt7,pt8], np.int32)
pts_L4 = pts_L4.reshape((-1,1,2))

# Удаление теней
fgbg = cv2.createBackgroundSubtractorMOG2(detectShadows = True)

# Структурирующие элементы для морфологических фильтров
kernelOp = np.ones((3,3), np.uint8)
kernelOp2 = np.ones((5,5), np.uint8)
kernelCl = np.ones((11,11), np.uint8)

# Переменные *
font = cv2.FONT_HERSHEY_SIMPLEX
persons = []
max_p_age = 5
pid = 1

while stream.isOpened():
##for image in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
	# Чтение кадра из источника видео stream
	grabbed, frame = stream.read()
	if not grabbed:
		break
##    frame = image.array

	########################################
	# Операции с входным видео
	height, width, _ = frame.shape
	frame = imutils.resize(frame, int(width // resize), int(height // resize)) # resize
	frame = imutils.rotate_bound(frame, int(rotate_degree)) # rotate 
	########################################

	for i in persons:
		i.age_one() # Возраст  каждого человека за кадр
	#################################
	#   Предварительная обработка   #
	#################################
	
	# Удаление фона
	fgmask = fgbg.apply(frame)
	fgmask2 = fgbg.apply(frame)

	# Преобразование в бинарный формат для удаления теней
	try:
		grabbed,imBin= cv2.threshold(fgmask,200,255,cv2.THRESH_BINARY)
		grabbed,imBin2 = cv2.threshold(fgmask2,200,255,cv2.THRESH_BINARY)
		# Открытие (размытие -> расширение) для удаления шума.
		mask = cv2.morphologyEx(imBin, cv2.MORPH_OPEN, kernelOp)
		mask2 = cv2.morphologyEx(imBin2, cv2.MORPH_OPEN, kernelOp)
		# Закрыть (расширение -> размытие) для соеденения белых областей.
		mask =  cv2.morphologyEx(mask , cv2.MORPH_CLOSE, kernelCl)
		mask2 = cv2.morphologyEx(mask2, cv2.MORPH_CLOSE, kernelCl)
	except:
		print('EOF') ###
		print('ВЫШЛО:', cnt_up)
		print ('ЗАШЛО:', cnt_down)
		break
	###############
	#   Контуры   #
	###############
	
	# RETR_EXTERNAL возвращает только сжатые внешние флаги. Все дочерние контуры остаются позади.
	contours0, hierarchy = cv2.findContours(mask2,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
	for cnt in contours0:
		area = cv2.contourArea(cnt)
		if area > areaTH:
			##################
			#  Отслеживание  #
			##################
			
			# Пока нет исключений для определения и подсчёта нескольких человек (находящихся близко друг к другу)
			# Но пока это и не нужно
			
			M = cv2.moments(cnt)
			cx = int(M['m10']/M['m00'])
			cy = int(M['m01']/M['m00'])
			x,y,w,h = cv2.boundingRect(cnt)

			new = True
			if cy in range(up_limit,down_limit):
				for i in persons:
					if abs(x-i.getX()) <= w and abs(y-i.getY()) <= h:
						# Объект похож на тот, что был ранее 
						new = False
						i.updateCoords(cx,cy)   # Обновляет координаты объекта и сбрасывает возраст
						if i.going_UP(line_down,line_up) == True:
							cnt_up += 1
							print("ID:",i.getId(), 'ВЫШЕЛ В -', time.strftime("%c"))
							log.write("ID: " + str(i.getId()) + 'ВЫШЕЛ В -' + time.strftime("%c") + '\n')
						elif i.going_DOWN(line_down,line_up) == True:
							cnt_down += 1
							print( "ID:",i.getId(),'ВОШЕЛ В -',time.strftime("%c"))
							log.write("ID: " + str(i.getId()) + 'ВОШЕЛ В -' + time.strftime("%c") + '\n')
						break
					if i.getState() == '1':
						if i.getDir() == 'down' and i.getY() > down_limit:
							i.setDone()
						elif i.getDir() == 'up' and i.getY() < up_limit:
							i.setDone()
					if i.timedOut():
						# Удалить i из списка человек
						index = persons.index(i)
						persons.pop(index)
						del i     # Освобождения памяти от i
				if new == True:
					p = Person.MyPerson(pid,cx,cy, max_p_age)
					persons.append(p)
					pid += 1     
			############################
			#   Выделение человека     #
			############################
			cv2.circle(frame,(cx,cy), 5, (0,0,255), -1) # Точка в центре объекта
			#img = cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),2) # Рисование прямоугольника 
			img = cv2.rectangle(frame,(x,y), (x+w,y+h), rectangle_color, rectangle_thickness) # Рисование прямоугольника 
			#cv2.drawContours(frame, cnt, -1, (0,255,0), 3) # Рисование контуров объекта
			
	#END for cnt in contours0
			
	#########################
	#    Рисование пути     #
	#########################
	for i in persons:
##        if len(i.getTracks()) >= 2:
##            pts = np.array(i.getTracks(), np.int32)
##            pts = pts.reshape((-1,1,2))
##            frame = cv2.polylines(frame,[pts],False,i.getRGB())
##        if i.getId() == 9:
##            print str(i.getX()), ',', str(i.getY())
		cv2.putText(frame, str(i.getId()),(i.getX(),i.getY()),font,0.3,i.getRGB(),1,cv2.LINE_AA)
		
	##########################
	#   Действия с кадрами   #
	##########################
	str_up = 'UP: '+ str(cnt_up)
	str_down = 'DOWN: '+ str(cnt_down)
	frame = cv2.polylines(frame,[pts_L1],False,line_down_color,thickness=2)
	frame = cv2.polylines(frame,[pts_L2],False,line_up_color,thickness=2)
	frame = cv2.polylines(frame,[pts_L3],False,(255,255,255),thickness=1)
	frame = cv2.polylines(frame,[pts_L4],False,(255,255,255),thickness=1)
	cv2.putText(frame, str_up , (10,40), font, 0.5, (255,255,255), 2, cv2.LINE_AA)
	cv2.putText(frame, str_up , (10,40), font, 0.5, (0,0,255), 1, cv2.LINE_AA)
	cv2.putText(frame, str_down , (10,90), font, 0.5, (255,255,255), 2, cv2.LINE_AA)
	cv2.putText(frame, str_down , (10,90), font, 0.5, (255,0,0), 1, cv2.LINE_AA)
	# display realtime fps
	new_frame_time = time.time()
	fps = 1/(new_frame_time - prev_frame_time)
	prev_frame_time = new_frame_time
	print(fps)

	fps = str(int(fps))
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

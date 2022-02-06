import cv2
import time
from nonloopvars import areaTH, up_limit, down_limit, line_down, line_up, log
import Person

from .obj_info_drawing import ObjInfoDraw

def contours(frame, mask2, persons, pid, max_p_age):

	is_up   = False
	is_down = False

	###############
	#   Контуры   #
	###############
	
	# RETR_EXTERNAL возвращает только сжатые внешние флаги. Все дочерние контуры остаются позади.
	contours0, hierarchy = cv2.findContours(mask2, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
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
			x, y, w, h = cv2.boundingRect(cnt)

			new = True
			if cy in range(up_limit, down_limit):
				for i in persons:
					if abs(x-i.getX()) <= w and abs(y-i.getY()) <= h:
						# Объект похож на тот, что был ранее 
						new = False
						i.updateCoords(cx, cy)   # Обновляет координаты объекта и сбрасывает счётчик
						if i.going_UP(line_down, line_up) == True:
							is_up = True
							print("ID:", i.getId(), 'ВЫШЕЛ В -', time.strftime("%c"))
							log.write("ID: " + str(i.getId()) + 'ВЫШЕЛ В -' + time.strftime("%c") + '\n')
						elif i.going_DOWN(line_down, line_up) == True:
							is_down = True
							print( "ID:", i.getId(), 'ВОШЕЛ В -', time.strftime("%c"))
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
						del i # Удаление переменной i из памяти
				if new == True:
					p = Person.MyPerson(pid, cx, cy, max_p_age)
					persons.append(p)
					pid += 1

			# Рисование точки(круга)
			ObjInfoDraw(frame).circle(cx, cy)
			# Рисование прямоугольника
			ObjInfoDraw(frame).rectangle((x, y), (w, h))
			# Рисование пути объекта линеей 
			#ObjInfoDraw(frame).way(persons)
			# Рисование id объекта 
			ObjInfoDraw(frame).id(persons)
			
	#END for cnt in contours0
	return frame, is_up, is_down
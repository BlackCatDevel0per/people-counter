import cv2
from config import Config
import numpy as np
from nonloopvars import font

from nonloopvars import rectangle_color, rectangle_thickness, obj_number_font_size

class ObjInfoDraw:
	#########################
	#   Выделение объекта   #
	#########################
	def __init__(self, frame):
		self.frame = frame

	def rectangle(self, xy: tuple, wh: tuple):
		x, y = xy
		w, h = wh
		#img = cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2) # Рисование прямоугольника 
		img = cv2.rectangle(self.frame, (x, y), (x+w, y+h), rectangle_color, rectangle_thickness) # Рисование прямоугольника 

	def circle(self, cx, cy):		
		cv2.circle(self.frame, (cx, cy), 5, (0, 0, 255), -1) # Точка в центре объекта


	def way(self, persons):
		for i in persons:
			# Рисование пути
			if len(i.getTracks()) >= 2:
				pts = np.array(i.getTracks(), np.int32)
				pts = pts.reshape((-1, 1, 2))
				self.frame = cv2.polylines(self.frame, [pts], False, i.getRGB())
			if i.getId() == 9:
				print(str(i.getX()), ',', str(i.getY()))

	def id(self, persons):
		for i in persons:
			# Рисование ID в центре объекта
			cv2.putText(self.frame, str(i.getId()), (i.getX(), i.getY()), 
						font, obj_number_font_size, i.getRGB(), 1, cv2.LINE_AA)

	def contours(self, cnt):
		cv2.drawContours(self.frame, cnt, -1, (0, 255, 0), 3) # Рисование контуров объекта
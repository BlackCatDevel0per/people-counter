import cv2
import numpy as np
from vars import font
from config import Config

obj_number_font_size = Config().get("obj_number_font_size")

def wdraw(frame, persons):
	#########################
	#    Рисование пути     #
	#########################
	for i in persons:
		# Рисование пути
		if len(i.getTracks()) >= 2:
			pts = np.array(i.getTracks(), np.int32)
			pts = pts.reshape((-1, 1, 2))
			frame = cv2.polylines(frame, [pts], False, i.getRGB())
		if i.getId() == 9:
			print(str(i.getX()), ',', str(i.getY()))
		# Рисование ID в центре объекта
		cv2.putText(frame, str(i.getId()), (i.getX(), i.getY()), 
					font, obj_number_font_size, i.getRGB(), 1, cv2.LINE_AA)
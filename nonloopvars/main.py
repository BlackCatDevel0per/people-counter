import cv2
import numpy as np
from config import Config

from sql import generate_uuid

# Size properties
##stream.set(3, 160) #Width
##stream.set(4, 120) #Height

# Raspberry Pi properties
#camera = PiCamera()
##camera.resolution = (160, 120)
##camera.framerate = 5
##rawCapture = PiRGBArray(camera, size=(160, 120))
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

#line_down_color = (255, 0, 0)
#line_up_color = (0, 0, 255)
line_down_color = Config().get("line_down_color")
line_down_bcolor = Config().get("line_down_bcolor")
line_up_color = Config().get("line_up_color")
line_up_bcolor = Config().get("line_up_bcolor")

# Object Options
rectangle_color = Config().get("rectangle_color")
rectangle_thickness = Config().get("rectangle_thickness")
obj_number_font_size = Config().get("obj_number_font_size")

# Other Options
sleep_time_minutes = Config().get("sleep_time_minutes")
sleep_motion_sensitivity = Config().get("sleep_motion_sensitivity")
mdt = Config().get("mdt")
sleep_enable = Config().get("sleep_enable")

pt1 = [0, line_down]
pt2 = [w, line_down]
pts_L1 = np.array([pt1, pt2], np.int32)
pts_L1 = pts_L1.reshape((-1, 1, 2))
pt3 = [0, line_up]
pt4 = [w, line_up]
pts_L2 = np.array([pt3, pt4], np.int32)
pts_L2 = pts_L2.reshape((-1, 1, 2))

pt5 = [0, up_limit]
pt6 = [w, up_limit]
pts_L3 = np.array([pt5, pt6], np.int32)
pts_L3 = pts_L3.reshape((-1, 1, 2))
pt7 = [0, down_limit]
pt8 = [w, down_limit]
pts_L4 = np.array([pt7, pt8], np.int32)
pts_L4 = pts_L4.reshape((-1, 1, 2))

# Удаление теней и фона
fgbg = cv2.createBackgroundSubtractorMOG2(detectShadows = True)

# Структурирующие элементы для морфологических фильтров
kernelOp = np.ones((3, 3), np.uint8)
kernelOp2 = np.ones((5, 5), np.uint8)
kernelCl = np.ones((11, 11), np.uint8)

# Vars *
font = cv2.FONT_HERSHEY_SIMPLEX
persons = []
# Если кол. человек в списке persons становится больше max_p_age, то он удаляет из него элемент
# Макс. время(тик) ожидания выхода человека за пределы кадра
max_p_age = 5
pid = 1

# People count vars
cnt_all = 0
cnt_up = 0
cnt_down = 0

# fps vars
prev_frame_time = 0
new_frame_time = 0

#
current_uuid = generate_uuid()
new_current_uuid = generate_uuid
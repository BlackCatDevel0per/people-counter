import cv2
import time
from vars import font

from vars import line_down_color, line_up_color
from vars import line_down_bcolor, line_up_bcolor
from vars import pts_L1, pts_L2, pts_L3, pts_L4

class InfoDraw:
	##########################
	#   Действия с кадрами   #
	##########################

	def lines(frame):
		# Рисование линий
		frame = cv2.polylines(frame, [pts_L1], False, line_down_color, thickness=2)
		frame = cv2.polylines(frame, [pts_L2], False, line_up_color, thickness=2)
		frame = cv2.polylines(frame, [pts_L3], False, line_down_bcolor, thickness=1)
		frame = cv2.polylines(frame, [pts_L4], False, line_up_bcolor, thickness=1)
		
		return frame

	def way(frame, cnt_up, cnt_down):
		# Рисование счетчиков UP и DOWN
		str_up = 'UP: '+ str(cnt_up)
		str_down = 'DOWN: '+ str(cnt_down)
		cv2.putText(frame, str_up, (10, 40), font, 0.5, (255, 255, 255), 2, cv2.LINE_AA)
		cv2.putText(frame, str_up, (10, 40), font, 0.5, (0, 0, 255), 1, cv2.LINE_AA)
		cv2.putText(frame, str_down, (10, 90), font, 0.5, (255, 255, 255), 2, cv2.LINE_AA)
		cv2.putText(frame, str_down, (10, 90), font, 0.5, (255, 0, 0), 1, cv2.LINE_AA)

		return frame


	def fps(frame, ftime: tuple):
		prev_frame_time, new_frame_time = ftime
		# Рисование счетчика с текущим fps
		###########################
		new_frame_time = time.time()
		fps = 1/(new_frame_time - prev_frame_time)
		prev_frame_time = new_frame_time

		fps = str(int(fps))
		cv2.putText(frame, f"FPS: {fps}", (220, 25), font, 0.5, (255, 255, 255), 2, cv2.LINE_AA)
		cv2.putText(frame, f"FPS: {fps}", (220, 25), font, 0.5, (0, 0, 255), 1, cv2.LINE_AA)
		###########################

		return new_frame_time, prev_frame_time
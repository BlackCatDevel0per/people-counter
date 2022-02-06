##from picamera.array import PiRGBArray
##from picamera import PiCamera
import cv2

# Изменение настроек не применяются во время работы программы

# Источник видео
#stream = cv2.VideoCapture(0)

# stream = cv2.VideoCapture("http://192.168.1.104:4747/video") # DroidCamX
#stream = cv2.VideoCapture('Test Files/TestVideo.avi')
stream = cv2.VideoCapture('Test Files/TestVedeo2.mp4')

from nonloopvars import persons, pid, max_p_age
from nonloopvars import log
from frames import vidops
from frames import binarize
from frames import contours
from frames import InfoDraw

# Импорт переменных счётчиков
from nonloopvars import cnt_up, cnt_down
from nonloopvars import prev_frame_time, new_frame_time

from nonloopvars import line_down, line_up
print("Red line y:", str(line_down))
print("Blue line y:", str(line_up))

while stream.isOpened():
    # for image in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
    # Чтение кадра из источника видео stream
    grabbed, frame = stream.read()
    if not grabbed:
        break
    #frame = image.array

    frame = vidops(frame)

    for i in persons:  # Слежение выхода за кадр каждого человека за кадр
        i.age_one()

    # Преобразование в бинарный формат для удаления теней
    frame, mask, mask2 = binarize(frame, grabbed)
    """
	try:
		frame, mask, mask2 = binarize(frame, grabbed)
	except Exception as e:
		print(e)
		print('EOF') ###
		print('ВЫШЛО:', cnt_up)
		print ('ЗАШЛО:', cnt_down)
		break
	"""

    frame, is_up, is_down = contours(frame, mask2, persons, pid, max_p_age)
    if is_up:
        cnt_up += 1
    elif is_down:
        cnt_down += 1

    # Рисование линий счётчика (на его работу не влияет)
    frame = InfoDraw.lines(frame)
    # Рисование счётчиков UP и DOWN
    frame = InfoDraw.count(frame, cnt_up, cnt_down)
    # Переменные для работы счётчика fps
    new_frame_time, prev_frame_time = InfoDraw.fps(
        frame, (prev_frame_time, new_frame_time))

    # Вывод кадров
    cv2.imshow('Stream', frame)
    #cv2.imshow('Mask', mask)

    if cv2.waitKey(1) & 0xFF == ord('q'):  # Завершение цикла на 'q'
        break

###############
#   Очистка   #
###############
log.flush()
log.close()

stream.release()
cv2.destroyAllWindows()

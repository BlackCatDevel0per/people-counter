import cv2

def SleepMotion(frame, frame2, sens: int):

	# frame2 is deltaframe
	#cv2.imshow('window',frame2)

	gray2 = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
	gray2 = cv2.GaussianBlur(gray2, (21, 21), 0)
	
	deltaframe=cv2.absdiff(frame2,gray2)
	#cv2.imshow('delta',deltaframe)
	threshold = cv2.threshold(deltaframe, 25, 255, cv2.THRESH_BINARY)[1]
	threshold = cv2.dilate(threshold,None)
	#cv2.imshow('threshold',threshold)
	countour,heirarchy = cv2.findContours(threshold, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
	for i in countour:
		if cv2.contourArea(i) > sens:
			return False
		return True
		"""
			return True
			break
		else:
			return False
 		"""
		#(x, y, w, h) = cv2.boundingRect(i)
		#cv2.rectangle(frame2, (x, y), (x + w, y + h), (255, 0, 0), 2)
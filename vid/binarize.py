import cv2
from vars import fgbg, kernelOp, kernelCl

def binarize(frame, grabbed):

	#################################
	#   Предварительная обработка   #
	#################################

	# Удаление фона
	fgmask = fgbg.apply(frame)
	fgmask2 = fgbg.apply(frame)

	grabbed, imBin= cv2.threshold(fgmask, 200, 255, cv2.THRESH_BINARY)
	grabbed, imBin2 = cv2.threshold(fgmask2, 200, 255, cv2.THRESH_BINARY)
	# Открытие (размытие -> расширение) для удаления шума.
	mask = cv2.morphologyEx(imBin, cv2.MORPH_OPEN, kernelOp)
	mask2 = cv2.morphologyEx(imBin2, cv2.MORPH_OPEN, kernelOp)
	# Закрыть (расширение -> размытие) для соеденения белых областей.
	mask =  cv2.morphologyEx(mask , cv2.MORPH_CLOSE, kernelCl)
	mask2 = cv2.morphologyEx(mask2, cv2.MORPH_CLOSE, kernelCl)

	return frame, mask, mask2
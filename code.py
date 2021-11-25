#importing required libraries
import cv2
import numpy
import time


#capturing background from webcam
capture = cv2.VideoCapture(0)  
#giving time to webcam to warm up
time.sleep(3)
background=0
for i in range(30):
	ret,background = capture.read()

#flipping the background
background = numpy.flip(background,axis=1)

while(capture.isOpened()):
    #capturing the live frame
	ret, img = capture.read()
	
	# Flipping the image 
	img = numpy.flip(img,axis=1)
	
	# Converting image to HSV color space.
	hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
	
	# Range for lower red
	red_lower = numpy.array([0,120,70])
	red_upper = numpy.array([10,255,255])
	mask1 = cv2.inRange(hsv,red_lower,red_upper)
	
	# Range for upper red
	red_lower = numpy.array([170,120,70])
	red_upper = numpy.array([180,255,255])
	mask2 = cv2.inRange(hsv,red_lower,red_upper)
	
	# Adding the two masks in order to generate the final mask.
	mask = mask1+mask2
	mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, numpy.ones((5,5),numpy.uint8))
	
	# Replacing pixels corresponding to cloak with the background pixels.
	img[numpy.where(mask==255)] = background[numpy.where(mask==255)]
	cv2.imshow('Invisibility cloak',img)  
	k = cv2.waitKey(10)
	if k == 27: # Esc key to stop
		break

# Release webcam 
capture.release()
# De-allocating any associated memory usage  
cv2.destroyAllWindows()

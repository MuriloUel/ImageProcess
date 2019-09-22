import numpy as np
import cv2 as cv
from scipy import ndimage as ndi

#Img read 
#img = cv.imread("imgs/pears.png")

#img chanell or gray
#gray = cv.cvtColor(img,cv.COLOR_BGR2GRAY)
#gray = cv.medianBlur(gray,3)

def my_wathershed(img,gray):

	kernel = np.ones((5,5),np.uint8)

	#Find the morphologycal gradient
	gradient = cv.morphologyEx(gray, cv.MORPH_GRADIENT, kernel)

	# cv.imshow("Gradient img",gradient)
	# cv.waitKey()

	#<Finding local max values>

	lm = ndi.filters.maximum_filter(gradient,size=8) #Finding the local max values
	msk = (gradient == lm) #// convert local max values to binary mask

	rows, cols = msk.shape

	mask = np.zeros((rows,cols),dtype=np.uint8)

	for i in range(rows):
		for j in range(cols):
			if msk[i,j]:
				mask[i,j] = 255
			else:
				mask[i,j] = 0

	#</Finding local max values>

	ret, markers = cv.connectedComponents(mask)#This function return a array marking each conected objetc with a value starting from 1, and 0 the rest

	# cv.imshow("markers",mask)
	# cv.waitKey()

	#Finaly we aplly the watershed segmentation
	markers = cv.watershed(img,markers) #this fucntion return -1 where there is a border
	# img[markers == -1] = [0,0,255]#marking the border in red on the original image

	# cv.imshow("watershed Final stage",img)
	# cv.waitKey()
	return markers
#Now we can find all the masks and try to find the values in the gray scale. Doing so, we can find the max value and the min value
#finding the distance value, like it was a 2D surface 

#======================================================JUST SHOWING ALL MASKS ONE BY ONE FOR FUN==============================================#
# print(np.unique(markers))

# mascaras = np.zeros((rows,cols),dtype=np.uint8)
# for value in np.unique(markers):
# 	if value != -1:
# 		mascaras[markers == value] = 255

# 	cv.imshow("watershed segments",mascaras)
# 	cv.waitKey()
# 	if value == 5:
# 		break


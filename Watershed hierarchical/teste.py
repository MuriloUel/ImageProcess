import numpy as np
import cv2 as cv
from watershed_Mosaic import my_wathershed
from find_mask_values import mask_values, find_neighbor, clean_Marker

def get_indexes_min_value(l):
	min_value = np.amin(np.array(l),axis=0)[3]#Getting the min_val from distance
	print(min_value)
	return [i for i, x in enumerate(l) if x[3] == min_value]
	


#Img read 
img = cv.imread("imgs/pears.png")

#img chanell or gray
gray = cv.cvtColor(img,cv.COLOR_BGR2GRAY)

markers = my_wathershed(img= img,gray=gray)

for i in range(1000):
	markers[markers==i] = 0

r,c = gray.shape

aaa = np.zeros((r,c,3),dtype=np.uint8)
aaa.fill(255)
aaa[markers==-1] = [0,0,255]
cv.imshow("watershed_inicial_stage",aaa)
cv.waitKey()




# img2 = img.copy()
# print(np.unique(markers))
# for aux in np.unique(markers):
# 	color = list(np.random.choice(range(256), size=3))#random color
# 	img2[markers == aux] = color#marking the border in red on the original image
# img2[markers == -1] = [0,0,255]
# cv.imshow("watershed_inicial_stage",img2)
# cv.waitKey()
import cv2 as cv
import numpy as np 

def mask_values(markers,gray):
	vet_dist = []
	rows, cols = gray.shape

	kernel = np.ones((3,3),np.uint8)
	#Find the morphologycal gradient
	gradient = cv.morphologyEx(gray, cv.MORPH_GRADIENT, kernel)
	for value in np.unique(markers):
		if value != -1:
			
			#Creating the mask
			mask = np.zeros((rows,cols),dtype=np.uint8)
			mask.fill(255)
			mask[markers == value] = 0
			
			sub = cv.subtract(gradient,mask)

			#Finding the min and max value from mask

			min_value = np.amin(sub)
			max_value = np.amax(sub)
			distance = max_value - min_value

			vet_dist.append([value,min_value,max_value,distance])
	
	return vet_dist

#row = int((index+1)/cols)
#col = ((index+1)%cols) -1

def find_neighbor(maks_number, markers):
	neighbor_mask_values = []
	row,col = np.where(markers == maks_number)#Finding all the pixels from this mask
	max_row, max_col = markers.shape
	for i in range(len(row)):
		r,c = row[i], col[i]
		
		if (r>2) and (c>2) and (markers[r-1,c-1] == -1):					#up left
			neighbor_mask_values.append(markers[r-2,c-2]) 			#appending mask value from up left neighbor
			neighbor_mask_values.append(markers[r-3,c-3]) 			#appending mask value from up left neighbor

		if (r>2) and (markers[r-1,c] == -1):							#up center
			neighbor_mask_values.append(markers[r-2,c]) 			#appending mask value from up center neighbor
			neighbor_mask_values.append(markers[r-3,c]) 			#appending mask value from up center neighbor

		if (r>2) and (c<max_col-3) and (markers[r-1,c+1] == -1):			#up right
			neighbor_mask_values.append(markers[r-2,c+2]) 			#appending mask value from up right neighbor
			neighbor_mask_values.append(markers[r-3,c+3]) 			#appending mask value from up right neighbor

		if (c<max_col-3) and (markers[r,c+1] == -1):					#center right
			neighbor_mask_values.append(markers[r,c+2]) 			#appending mask value from center right neighbor
			neighbor_mask_values.append(markers[r,c+3]) 			#appending mask value from center right neighbor

		if (r<max_row-3) and (c<max_col-3) and (markers[r+1,c+1] == -1):	#down right
			neighbor_mask_values.append(markers[r+2,c+2]) 			#appending mask value from down right neighbor
			neighbor_mask_values.append(markers[r+3,c+3]) 			#appending mask value from down right neighbor

		if (r<max_row-3) and (markers[r+1,c] == -1):					#down center
			neighbor_mask_values.append(markers[r+2,c]) 			#appending mask value from down center neighbor
			neighbor_mask_values.append(markers[r+3,c]) 			#appending mask value from down center neighbor

		if (r<max_row-3) and (c>2) and (markers[r+1,c-1] == -1):			#down left
			neighbor_mask_values.append(markers[r+2,c-2]) 			#appending mask value from down left neighbor
			neighbor_mask_values.append(markers[r+2,c-2]) 			#appending mask value from down left neighbor

		if (c>2) and (markers[r,c-1] == -1):							#center left
			neighbor_mask_values.append(markers[r,c-2]) 			#appending mask value from center left neighbor
			neighbor_mask_values.append(markers[r,c-2]) 			#appending mask value from center left neighbor

	neighbor_mask_values = list(np.unique(neighbor_mask_values)) #Removing repeated masks values
	if -1 in neighbor_mask_values:
		neighbor_mask_values.pop(neighbor_mask_values.index(-1))#Removing -1 value, cause it is not a mask number
	if maks_number in neighbor_mask_values:
		neighbor_mask_values.pop(neighbor_mask_values.index(maks_number))#Removing it self
	return neighbor_mask_values

def clean_Marker(markers):
	rows,cols = markers.shape
	for r in range(rows):
		for c in range(cols):

			if markers[r,c] == -1:
				if r>0 and c>0 and r<rows-1 and c<cols-1:
					if (markers[r-1,c-1] == markers[r+1,c+1]) and (markers[r-1,c-1] != -1): #up left / down right
						markers[r,c] = markers[r-1,c-1]
						
					if (markers[r+1,c-1] == markers[r-1,c+1]) and (markers[r+1,c-1] != -1): #down left / up right
						markers[r,c] = markers[r+1,c-1]
						
				if c>0 and c<cols-1:
					if (markers[r,c-1] == markers[r,c+1]) and (markers[r,c-1] != -1):       #left / right 
						markers[r,c] = markers[r,c-1]
						
				if r>0 and r<rows-1:
					if (markers[r-1,c] == markers[r+1,c]) and (markers[r-1,c] != -1):       #up / down
						markers[r,c] == markers[r-1,c]


	return markers





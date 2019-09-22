import numpy as np
import cv2 as cv
from watershed_Mosaic import my_wathershed
from find_mask_values import mask_values, find_neighbor, clean_Marker

def get_indexes_min_value(l):
	min_value = np.amin(np.array(l),axis=0)[3]#Getting the min_val from distance
	return [i for i, x in enumerate(l) if x[3] == min_value]
	

#Img read 
img = cv.imread("imgs/car.jpeg")

#img chanell or gray
gray = cv.cvtColor(img,cv.COLOR_BGR2GRAY)

#gray = cv.GaussianBlur(gray,(3,3),0,0)
gray = cv.blur(gray,(3,3))
#gray = cv.medianBlur(gray,3)


markers = my_wathershed(img= img,gray=gray)

vet_distance = mask_values(markers = markers, gray = gray)#Return a list [mask value, min gray val, max gray val, distance]

Nothing_to_merge = False
hierarchy_number = 50

cont = 0 
for hierarchy in range(hierarchy_number):

	indexes = get_indexes_min_value(vet_distance) #List with all of the indexes with the lowest distance value
	#So, index have all the indices with the lowest value of distance. it's type is list
	#We need to change this for the mask number, so we can pop the merged mask without mess up with the index
	lowest_vet_dist = []
	for index in indexes:
		lowest_vet_dist.append(vet_distance[index])

	Merged_maks = []
	for lowest in lowest_vet_dist:
		if not (lowest in Merged_maks):#if this index was not already merged
			neighbor_mask_values = find_neighbor(lowest[0],markers)#aplly the value mask from the menimun value index and markers to find the neighbor
			#Now neighbor_mask_values has all the mask values from all neighbor of the actual lowest distance mask

			neighbor_to_merge =[[0,0,0,300]]#Starting neighbor to merge; [value,min gray val,max gray val, distance]
			#neighbor_to_merge_index = []

			for neighbor_value in neighbor_mask_values:#Find the biggest distance value from all the neighbor
				
				neighbor_index = [i for i,x in enumerate(vet_distance) if x[0] == neighbor_value] #Find the index of neighbor in vet_dist
				#if neighbor_index != []:
				neighbor_index = neighbor_index[0]
			
				actual_neighbor_distance = vet_distance[neighbor_index][3]#actual neigbor distance

				if actual_neighbor_distance == neighbor_to_merge[0][3]:
					neighbor_to_merge.append(vet_distance[neighbor_index])
					#neighbor_to_merge_index.append(neighbor_index)
				if actual_neighbor_distance < neighbor_to_merge[0][3]: #If actual neighbor distance > last one
					neighbor_to_merge = [vet_distance[neighbor_index]] #att neighbor to merge
					#neighbor_to_merge_index = [neighbor_index]
				
			#Here, neighbor_to_merge has a list of the mask value , min/max values of gradient lvl and the distance of all the neighbors to merge

			new_min = 300 #A value tha will never happens, cause pixel values are until 255
			new_max = 0

			# #Start merging them!
			value_of_the_new_mask = lowest[0]

			for n_t_m in neighbor_to_merge:
				markers[markers == n_t_m[0]] = value_of_the_new_mask #Masks with bigger dist are being merged with the lowest one
				#Saving new min/max values
							
				if n_t_m[1] < new_min:
					new_min = n_t_m[1]
				if n_t_m[2] > new_max:
					new_max = n_t_m[2]
				Merged_maks.append(n_t_m)
				if n_t_m not in vet_distance:
					Nothing_to_merge = True
					break
				vet_distance.pop(vet_distance.index(n_t_m))

			new_dis = new_max - new_min

			Merged_maks.append(lowest)
			#Removing the lowest mask from vet_distance
			vet_distance.pop(vet_distance.index(lowest))#Pop the lowest neighbor
			#Putting back to the vet_distance the new mask merged
			new_mask = [value_of_the_new_mask,new_min,new_max,new_dis]
			vet_distance.append(new_mask)
			#now, we have the vet_dist updated and the markers masks are merged... we just need to remove the -1 lines between the merged masks
		if Nothing_to_merge:
			break		
	# cont+=1
	# if (cont%10) == 0:
	# 	img2 = img.copy()
	# 	for aux in np.unique(markers):
	# 		if aux != -1:
	# 			color = list(np.random.choice(range(256), size=3))#random color
	# 			img2[markers == aux] = color
	# 	#img2[markers == -1] = [0,0,255]
	# 	cv.imshow("watershed_final_stage_"+str(cont),img2)
	# 	cv.waitKey()
	# 	cv.destroyAllWindows()

	if Nothing_to_merge:
		print("Nothing to merge on hierarchy :",hierarchy )
		break
markers = clean_Marker(markers)

img2 = img.copy()
# for aux in np.unique(markers):
# 	if aux != -1:
# 		color = list(np.random.choice(range(256), size=3))#random color
# 		img2[markers == aux] = color
img2[markers == -1] = [0,0,255]
cv.imshow("watershed_final_stage_",img2)
cv.waitKey()
cv.imwrite("watershed_final_stage_blur_k7_"+str(hierarchy)+".jpeg",img2)


#After find all the neighbor, find the one with bigger distance and turn both the same (as numeric in the markers), reculculate the  
#distance of the new mask and repeat the process as many times as hierarchy 
#after all this merging process end, pass through the markers, line by line, finding the -1 values and check if the cols-1 and the 
#col+1 have the same value, if so, turn the -1 in this value, repeat for cols
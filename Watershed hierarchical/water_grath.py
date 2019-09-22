import cv2 as cv
import numpy as np 
from find_mask_values import find_neighbor
from watershed_Mosaic import my_wathershed
from scipy import ndimage as ndi

def try_one(graph):

	lowest_vertex = []
	lowest_gradient_value = 300 #a impossible big gradient value

	#find all the vertexs with the lowest value and append them in the lowest_vertex list
	for vertex in graph:
		if vertex[1] == lowest_gradient_value:
			lowest_vertex.append(vertex)
		if vertex[1] < lowest_gradient_value:
			lowest_gradient_value = vertex[1]#att the lowest gradient value with the new one
			lowest_vertex = [vertex] #Create a new list with the new lowest gradient found

	#now, the lowest_vertex list has all the vertexs with the lowest gradient value

	new_markers = np.zeros((gray.shape), dtype=np.uint8)#Creating a new black mask

	for vertex in lowest_vertex:
		for neighbors in vertex[2]:
			new_markers = add_line_to_marker(neighbors = neighbors,graph = graph,markers = markers,new_markers= new_markers)
	cv.imshow("new_mask",new_markers)
	cv.waitKey()
	return new_markers

def add_line_to_marker(neighbors,graph,markers,new_markers):
	row,col = np.where(markers == neighbors[0])#Finding all the pixels from this mask
	max_row, max_col = markers.shape
	for i in range(len(row)):
		r,c = row[i], col[i]
		value = neighbors[1]
		if (r>2) and (c>2) and (markers[r-1,c-1] == -1):					#up left
			if markers[r-2,c-2] == value:			#appending mask value from up left neighbor
				new_markers[r-1,c-1] = 255
			elif markers[r-3,c-3] == value:			#appending mask value from up left neighbor
				new_markers[r-1,c-1] = 255

		if (r>2) and (markers[r-1,c] == -1):							#up center
			if markers[r-2,c] == value:	#appending mask value from up center neighbor
				new_markers[r-1,c] = 255
			elif markers[r-3,c] == value:	#appending mask value from up center neighbor
				new_markers[r-1,c] = 255

		if (r>2) and (c<max_col-3) and (markers[r-1,c+1] == -1):			#up right
			if markers[r-2,c+2] == value:			#appending mask value from up right neighbor
				new_markers[r-1,c+1] = 255
			elif markers[r-3,c+3] == value:			#appending mask value from up right neighbor
				new_markers[r-1,c+1] = 255

		if (c<max_col-3) and (markers[r,c+1] == -1):					#center right
			if markers[r,c+2] == value:	#appending mask value from center right neighbor
				new_markers[r,c+1] = 255
			elif markers[r,c+3] == value:	#appending mask value from center right neighbor
				new_markers[r,c+1] = 255

		if (r<max_row-3) and (c<max_col-3) and (markers[r+1,c+1] == -1):	#down right
			if markers[r+2,c+2] == value:			#appending mask value from down right neighbor
				new_markers[r+1,c+1] = 255
			elif markers[r+3,c+3] == value:			#appending mask value from down right neighbor
				new_markers[r+1,c+1] = 255

		if (r<max_row-3) and (markers[r+1,c] == -1):					#down center
			if markers[r+2,c] == value:	#appending mask value from down center neighbor
				new_markers[r+1,c] = 255
			elif markers[r+3,c] == value:	#appending mask value from down center neighbor
				new_markers[r+1,c] = 255

		if (r<max_row-3) and (c>2) and (markers[r+1,c-1] == -1):			#down left
			if markers[r+2,c-2] == value:			#appending mask value from down left neighbor
				new_markers[r+1,c-1] = 255
			elif markers[r+2,c-2] == value:			#appending mask value from down left neighbor
				new_markers[r+1,c-1] = 255

		if (c>2) and (markers[r,c-1] == -1):							#center left
			if markers[r,c-2]	== value:	#appending mask value from center left neighbor
				new_markers[r,c-1] = 255
			elif markers[r,c-2] == value:	#appending mask value from center left neighbor
				new_markers[r,c-1] = 255
	return new_markers


def find_vertex_index(id_vertex,graph):
	for graph_index in range(len(graph)):
		if graph[graph_index][0] == id_vertex:
			return graph_index

def find_avarege_mask_value(mask_number,markers,gray):
	rows,cols = gray.shape
	mask = np.zeros((rows,cols),dtype=np.uint8)
	mask.fill(255)
	mask[markers == mask_number] = 0
	
	sub = cv.subtract(gray,mask)


	return int((sum(sum(sub)))/np.count_nonzero(sub))

img = cv.imread("imgs/car.jpeg")

#img chanell or gray
gray = cv.cvtColor(img,cv.COLOR_BGR2GRAY)

gray = cv.blur(gray,(3,3))

markers = my_wathershed(img= img,gray=gray)

graph = []#Starting the graph
#														  ID         gradient of mosaic image       List of neighbors vertex
#The graph is a list structured as follow:                 |                    |                             |
#														   v                    v                             V
#											[ [(mask_value1,maks_value2),gradient diference],        [ID, ID , ID ... ID]
#											                                     .
#											                                     .
#											                                     .
#											  [(mask_value1,maks_value2),gradient diference],        [ID, ID , ID ... ID] ]

# lines_already_computed = []

# for current_mask_number in list(np.unique(markers)):
# 	if current_mask_number != -1:
# 		#Find all the neigbor's numbers
# 		neighbors_number = find_neighbor(current_mask_number,markers)
# 		#find avarage gray number in current mask
# 		current_avarege_value = find_avarege_mask_value(current_mask_number,markers,gray)

# 		for neighbor in neighbors_number:
# 			#If we find a previous mask that was already computed and is it's neighbor, we don't need to recalculate this vertex
# 			if (neighbor,current_mask_number) in lines_already_computed:
# 				vertex_index = find_vertex_index((neighbor,current_mask_number),graph)
# 				for neighbor_aux in neighbors_number:
# 					if neighbor_aux != neighbor:
# 						if (neighbor_aux,current_mask_number) not in lines_already_computed:
# 							graph[vertex_index][2].append((current_mask_number,neighbor_aux))
# 			else:
# 				neighbor_avarage_value =  find_avarege_mask_value(neighbor,markers,gray)
# 				new_vertice = [(current_mask_number,neighbor),abs(neighbor_avarage_value - current_avarege_value),[]]
# 				for neighbor_aux in neighbors_number:
# 					if neighbor_aux != neighbor:
# 						new_vertice[2].append((current_mask_number,neighbor_aux))
# 				graph.append(new_vertice)
# 				lines_already_computed.append((current_mask_number,neighbor))

#print(graph)
id_already_computed = []
for current_mask_number in list(np.unique(markers)):
	if current_mask_number != -1:
		#Find all the neigbor's numbers
		neighbors_number = find_neighbor(current_mask_number,markers)
		#find avarage gray number in current mask
		current_avarege_value = find_avarege_mask_value(current_mask_number,markers,gray)

		for neighbor in neighbors_number:
			#If it was not already computed
			if (neighbor,current_mask_number) not in id_already_computed:
				neighbor_avarage_value =  find_avarege_mask_value(neighbor,markers,gray)
				new_vertice = [(current_mask_number,neighbor),abs(neighbor_avarage_value - current_avarege_value),[]]
				graph.append(new_vertice)
				id_already_computed.append((current_mask_number,neighbor))
for vertex in graph:
	for vertex2 in graph:
		if vertex != vertex2:
			if (vertex[0][0] in vertex2[0]) or (vertex[0][1] in vertex2[0]):# if vertex has any mask in comum with vertex2, they ae neihbors
				vertex[2].append(vertex2[0]) #add vertex2 id to vertex neighbor list

#Now, the graph has all the vertex between masks and his gradient's values and neighbors
#All we need to do is find all the vertex that have the lowest gradient and set him and his neihbor as a new mask for
#the new hierarchy of watershed

#print(graph)
new_markers = try_one(graph)


cv.imshow("new_mask",new_markers)
cv.waitKey()

#Transform this mask in a maks that ca be apllyed to watershed function
lm = ndi.filters.maximum_filter(new_markers,size=8) #Finding the local max values
msk = (new_markers == lm) #// convert local max values to binary mask

rows, cols = msk.shape

mask = np.zeros((rows,cols),dtype=np.uint8)

for i in range(rows):
	for j in range(cols):
		if msk[i,j]:
			mask[i,j] = 255
		else:
			mask[i,j] = 0

ret, new_markers = cv.connectedComponents(mask)#This function return a array marking each conected objetc with a value starting from 1, and 0 the rest
#End of tranformation


markers = cv.watershed(img,new_markers)

img[markers==-1]=[0,0,255]

cv.imshow("watershed",img)
cv.waitKey()




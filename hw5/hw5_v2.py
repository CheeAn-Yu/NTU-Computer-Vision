import numpy as np
import cv2
import pandas as pd
img=cv2.imread("Lena.jpg")
gray_img=cv2.imread("Lena.jpg",0)

def dil_kernal(img,row,col):
	value=[]
	for i in range(-2,3):
		for j in range(-2,3):
			if (i==-2 and j==-2) or (i==-2 and j==2)or(i==2 and j==-2)or(i==2 and j==2):
				pass
			else:
				value.append(img[row+i][col+j])
	return max(value)
def ero_kernal(img,row,col):
	value=[]
	for i in range(-2,3):
		for j in range(-2,3):
			if (i==-2 and j==-2) or (i==-2 and j==2)or(i==2 and j==-2)or(i==2 and j==2):
				pass
			else:
				value.append(img[row+i][col+j])
					
	return min(value)
def dilation(img):
	row=img.shape[0]
	col=img.shape[1]
	new=np.zeros((row+4,col+4),dtype=np.int)
	res=np.zeros((row,col),dtype=np.int)

	for i in range(row):
		for j in range(col):
			new[i+2][j+2]=img[i][j]

	for i in range(row):
		for j in range(col):
			res[i][j]=dil_kernal(new,i+2,j+2)
	return res
def erosion(img):
	row=img.shape[0]
	col=img.shape[1]
	new=np.zeros((row+4,col+4),dtype=np.int)
	res=np.zeros((row,col),dtype=np.int)
	for i in range(row):
		for j in range(col):
			new[i+2][j+2]=img[i][j]

	for i in range(row):
		for j in range(col):
				res[i][j]=ero_kernal(new,i+2,j+2)
	return res		
def opening(img):
	ero_im=erosion(img)
	open_im=dilation(ero_im)
	return open_im
def closing(img):
	dil_im=dilation(img)
	close_im=erosion(dil_im)
	return close_im



#cv2.imwrite("dilation.png",dilation(gray_img))
#cv2.imwrite("erosion.png",erosion(gray_img))
cv2.imwrite("opening.png",opening(gray_img))
cv2.imwrite("closing.png",closing(gray_img))
#print(new)
	#df=pd.DataFrame(new)
	#df2=pd.DataFrame(res)
	#df.to_csv("ori.csv")
	#df2.to_csv("dilation.csv")





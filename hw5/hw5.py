import numpy as np
import cv2
import pandas as pd
img=cv2.imread("Lena.jpg")
gray_img=cv2.imread("Lena.jpg",0)

def dil_kernal(img,new,row,col):
	value=[]
	for i in range(-2,3):
		for j in range(-2,3):
			if (i==-2 and j==-2) or (i==-2 and j==2)or(i==2 and j==-2)or(i==2 and j==2):
				pass
			else:
				if img[row][col]>img[row+i][col+j]:
					new[row+i][col+j]=img[row][col]
def ero_kernal(img,row,col):
	for i in range(-2,3):
		for j in range(-2,3):
			if (i==-2 and j==-2) or (i==-2 and j==2)or(i==2 and j==-2)or(i==2 and j==2):
				pass
			else:
				if img[row+i][col+j]!=255:
					return False
	return True
def dilation(img):
	row=img.shape[0]
	col=img.shape[1]
	new=np.zeros((row+4,col+4),dtype=np.int)
	res=np.zeros((row+4,col+4),dtype=np.int)

	for i in range(row):
		for j in range(col):
			new[i+2][j+2]=img[i][j]

	for i in range(row):
		for j in range(col):
			dil_kernal(new,res,i+2,j+2)
	print(new)
	df=pd.DataFrame(new)
	df2=pd.DataFrame(res)
	df.to_csv("ori.csv")
	df2.to_csv("dilation.csv")
	return res
def erosion(img):
	row=img.shape[0]
	col=img.shape[1]
	new=np.zeros((row+4,col+4),dtype=np.int)
	res=np.zeros((row,col),dtype=np.int)
	for i in range(row):
		for j in range(col):
			new[i+2][j+2]=img[i][j]

	for i in range(2,new.shape[0]):
		for j in range(2,new.shape[1]):
			if new[i][j]==255 and ero_kernal(new,i,j):
				res[i-2][j-2]=255
	return res		
def opening(img):
	ero_im=erosion(img)
	open_im=dilation(ero_im)
	return open_im
def closing(img):
	dil_im=dilation(img)
	close_im=erosion(dil_im)
	return close_im



cv2.imwrite("dilation.png",dilation(gray_img))
#cv2.imwrite("erosion.png",erosion(im_128))
#cv2.imwrite("opening.png",opening(im_128))
#cv2.imwrite("closing.png",closing(im_128))






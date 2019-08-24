import numpy as np
import cv2
import pandas as pd
img=cv2.imread("Lena.jpg")
bin_img=cv2.imread("Lena.jpg",0)


def bin_128(img):
	new=img.copy()
	row=img.shape[0]
	col=img.shape[1]
	for i in range(row):
		for j in range(col):
			if img[i][j]>=128:
				new[i][j]=255
			else:
				new[i][j]=0
	return new
im_128=bin_128(bin_img)

#cv2.imwrite("128.jpg",im_128)
def dil_kernal(img,row,col):
	for i in range(-2,3):
		for j in range(-2,3):
			if (i==-2 and j==-2) or (i==-2 and j==2)or(i==2 and j==-2)or(i==2 and j==2):
				pass
			else:
				img[row+i][col+j]=255
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
	res=np.zeros((row,col),dtype=np.int)

	for i in range(row):
		for j in range(col):
			if img[i][j]==255:
				dil_kernal(new,i+2,j+2)
	for i in range(row):
		for j in range(col):
			res[i][j]=new[i+2][j+2]
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

def hit_and_miss(img):
	#Ac
	row=img.shape[0]
	col=img.shape[1]
	new=np.zeros((row,col),dtype=np.int)
	Ac=np.zeros((row,col),dtype=np.int)
	new2=np.zeros((row,col),dtype=np.int)
	res=np.zeros((row,col),dtype=np.int)
	for i in range(row):
		for j in range(col):
			if img[i][j]==255:
				Ac[i][j]=0
			else:
				Ac[i][j]=255
	for i in range(row-1):
		for j in range(1,col):
			if img[i][j]==255 and img[i][j-1]==255 and img[i+1][j]==255:
				new[i][j]=255
	for i in range (1,row):
		for j in range(col-1):
			if Ac[i-1][j]==255 and Ac[i-1][j+1] and Ac[i][j+1]:
				new2[i][j]=255
	for i in range(row):
		for j in range(col):
			if new[i][j]==255 and new2[i][j]==255:
				res[i][j]=255
	return res

#cv2.imwrite("dilation.png",dilation(im_128))
#cv2.imwrite("erosion.png",erosion(im_128))
#cv2.imwrite("opening.png",opening(im_128))
#cv2.imwrite("closing.png",closing(im_128))
cv2.imwrite("hit_and_miss.png",hit_and_miss(im_128))





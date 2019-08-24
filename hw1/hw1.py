import cv2 
import numpy as np
img=cv2.imread('lena512.bmp')
imgh=img.shape[0]
imgw=img.shape[1]
def upside_down(img):
	new=img.copy()
	for i in range(imgh/2):
		for j in range(imgw):
			new[i][j]=img[-i][j]
			new[-i][j]=img[i][j]
	cv2.imwrite('lena_upside_down.jpg',new)
	return new
def left_right(img):
	new=img.copy()
	for i in range(imgh):
		for j in range(imgw/2):
			new[i][j]=img[i][-j]
			new[i][-j]=img[i][j]
	cv2.imwrite('lena_left_right.jpg',new)
	return new
def diag(img):
	new=img.copy()
	for i in range(imgh):
		for j in range(imgw):
			new[i][j]=img[j][i]
	cv2.imwrite('lena_diagonal.jpg',new)
	return new
def main():
	cv2.imshow("Image0",img)
	cv2.imshow('Image1',upside_down(img))
	cv2.imshow('Image2',left_right(img))
	cv2.imshow("Image3",diag(img))
	cv2.waitKey(0)
	
main()

#cv2.imshow("Image0",img)
#cv2.imshow('Image1',upside_down(img))
#cv2.imshow('Image2',left_right(img))
#cv2.imshow("Image3",diag(img))
#cv2.waitKey(0)
#cv2.destroyWindow()


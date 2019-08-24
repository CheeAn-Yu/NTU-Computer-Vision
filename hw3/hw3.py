import numpy as np
import cv2
import matplotlib.pyplot as plt
img=cv2.imread("Lena.jpg",0)
def draw_Histo(img):
	
	row=img.shape[0]
	col=img.shape[1]
	x=[i for i in range(256)]
	y=[0]*256
	for i in range(row):
		for j in range(col):
			y[img[i][j]]+=1
	plt.bar(x,y,align="center",alpha=0.5)
	plt.savefig("histogram_ori.jpg")
	plt.show()
def Histo_eq(img):
	nim=img.copy()
	row=img.shape[0]
	col=img.shape[1]
	n=row*col
	
	y=[0]*256
	s=[0]*256
	for i in range(row):
		for j in range(col):
			y[img[i][j]]+=1
	#print (y)
	s[0]=255*y[0]/n
	for i in range(1,256):
		s[i]=(s[i-1]+255*float(y[i])/n)
	#print(s)
	for i in range(row):
		for j in range(col):
			k=nim[i][j]
			nim[i][j]=s[k]
	#print(nim)
	cv2.imwrite("Histo_eq.jpg",nim)
	cv2.imshow("Histo_eq",nim)
	cv2.waitKey(0)
	draw_Histo(nim)

#Histo_eq(img)
draw_Histo(img)



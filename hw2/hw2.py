import numpy as np
import cv2 as cv
import matplotlib.pyplot as plt
img=cv.imread("lena512.bmp")
img_gray=cv.cvtColor(img, cv.COLOR_BGR2GRAY)
row=img.shape[0]
col=img.shape[1]
#test=np.array([[255,255,255,0,255,0],[0,0,255,0,255,0],[255,255,255,0,0,0],[0,255,0,255,0,0],[255,255,0,255,0,0]])
#test=np.array([[0,255,255,0,255,255,0,255],[0,255,255,0,255,255,0,255],[0,255,255,255,255,255,0,0]])
test=np.array([[255,255,255,0,255,255,0,255],[0,0,255,0,255,255,0,255],[255,255,255,0,255,255,0,255]])
#print (img[0][0],img[-512][-512])

def bin (img):
	for i in range(row):
		for j in range(col):
			if img[i][j]<128:
				img[i][j]=0
			else:
				img[i][j]=255
    
	#cv.imwrite("thresold_128.png",img)
	return img
def histogram(img):
	p=[0]*256
	x=[i for i in range(256)]
	print (x)
	for i in range(row):
		for j in range(col):
			p[img[i][j]]+=1
	plt.bar(x,p,align="center",alpha=0.5)
	plt.savefig("histogram.png")
	plt.show()
	
def connected(img):
	label=1
	im=bin(img)
	nim=img.copy()
	col=8
	row=3
	im=test
	for i in range(row):
		for j in range(col):
			if im[i][j]==255:
				im[i][j]=label
				label+=1
	check=1
	while check==1:
		check=0
		for j in range(1,col):
			if im[0][j]!=0:
				if im[0][j-1]!=im[0][j]:
					check=1
				im[0][j]=min(im[0][j-1],im[0][j])
		for i in range(1,row):#from left to right,up to down
			for j in range(col):
				if j==0 and im[i][j]!=0 and im[i-1][j]!=0:
					if im[i][j]!=im[i-1][j]:
						check=1
					im[i][j]=min(im[i][j],im[i-1][j])
				if im[i][j]!=0 and i>0 :
					if im[i][j]!=0 and im[i][j-1]!=0:
						if im[i][j]!=im[i][j-1]:
							check=1
						im[i][j]=min(im[i][j],im[i][j-1])
					if im[i][j]!=0 and im[i-1][j]!=0:
						if im[i][j]!=im[i-1][j]:
							check=1
						im[i][j]=min(im[i][j],im[i-1][j])

		for j in range(2,col):
			if im[-1][-j]!=0 and im[-1][-j+1]!=0:
				if im[-1][-j]!=im[-1][-j+1]:
					check=1
				im[-1][-j]=min(im[-1][-j],im[-1][-j+1])
		for i in range(2,row):
			for j in range(1,col):
				if j==1 and im[-i][-j]!=0 and im[-i+1][-j]!=0:
					if im[-i][-j]!=im[-i+1][-j]:
						check=1
					im[-i][-j]=min(im[-i][-j],im[-i+1][-j])
				if im[-i][-j]!=0 :
					if im[-i][-j]!=0 and im[-i+1][-j]!=0:
						if im[-i][-j]!=im[-i+1][-j]:
							check=1
						im[-i][-j]=min(im[-i][-j],im[-i+1][-j])
					if im[-i][-j]!=0 and im[-i][-j+1]!=0:
						if im[-i][-j]!= im[-i][-j+1]:
							check=1
						im[-i][-j]=min(im[-i][-j],im[-i][-j+1])

	area=[]
	for i in range(row):
		for j in range(col):
			if im[i][j]!=0:
				area.append(im[i][j])
	#print(im)
	for item in set(area):
		if area.count(item)>500:
			x=[]
			y=[]
			#print(x,y)
			for i in range(row):
				for j in range(col):
					if im[i][j]==item:
						x.append(j)
						y.append(i)
			print(min(x),min(y),max(x),max(y),item,area.count(item))
			cv.rectangle(nim,(min(x),min(y)),(max(x),max(y)),(55,25,155),4)
			
	#for item in set(area):
	#	x=[]
	#	y=[]
			#print(x,y)
	#	for i in range(row):
	#		for j in range(col):
	#			if im[i][j]==item:
	#				x.append(j)
	#				y.append(i)
	#	print(min(x),min(y),max(x),max(y),item,area.count(item))
		#cv.rectangle(nim,(min(x),min(y)),(max(x),max(y)),(55,25,155),4)
			
	print (im)		
	#cv.imwrite("connected.png",nim)
	return im

rest=connected(test)

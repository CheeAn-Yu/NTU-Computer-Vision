import numpy as np
import cv2 as cv
import matplotlib.pyplot as plt
import pandas as pd
#np.set_printoptions(threshold=np.inf)
img=cv.imread("Lena.jpg")
img_gray=cv.cvtColor(img, cv.COLOR_BGR2GRAY)
test=np.array([[255,255,255,255,0,0],[0,0,0,255,0,0],[255,0,0,255,0,0],[255,255,0,255,0,0],[255,255,0,255,0,0]])
#test=np.array([[0,255,255,0,255,255,0,255],[0,255,255,0,255,255,0,255],[0,255,255,255,255,255,0,0]])
#test=np.array([[255,255,255,0,255,255,0,255],[0,0,255,0,255,255,0,255],[255,255,255,0,255,255,0,255]])
#print (nimg[0][0],nimg[-512][-512])

def bin (img):
	row=img.shape[0]
	col=img.shape[1]
	for i in range(row):
		for j in range(col):
			if img[i][j]<128:
				img[i][j]=0
			else:
				img[i][j]=255
    
	#cv.nimwrite("thresold_128.png",nimg)
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
	row=img.shape[0]
	col=img.shape[1]
	label=1
	im=bin(img)

	nim=np.zeros((row,col),dtype=np.int)
	
	
	for i in range(row):
		for j in range(col):
			nim[i][j]=im[i][j]
			if nim[i][j]==255:
				nim[i][j]=label
				label+=1
	check=1
	while check==1:
		check=0
		for i in range(row):#from left to right,up to down
			for j in range(col):

				if i==0 and j-1>=0:
					if nim[i][j]!=0 and nim[i][j-1]!=0:
						if nim[i][j]!=nim[i][j-1]:
							check=1
						nim[i][j]=min(nim[i][j],nim[i][j-1])
						
				elif j==0 and i-1>=0:
					if nim[i][j]!=0 and nim[i-1][j]!=0:
						if nim[i][j]!=nim[i-1][j]:
							check=1
						nim[i][j]=min(nim[i][j],nim[i-1][j])
						
				elif i>0 and j>0:
					if nim[i][j]!=0 and nim[i-1][j]!=0:
						if nim[i][j]!=nim[i-1][j]:
							check=1
						nim[i][j]=min(nim[i][j],nim[i-1][j])
						
					if nim[i][j]!=0 and nim[i][j-1]!=0:
						if nim[i][j]!=nim[i][j-1]:
							check=1
						nim[i][j]=min(nim[i][j],nim[i][j-1])
						
			
				
		for i in range(1,row+1):
			for j in range(1,col+1):
				if i==1 and j>1:
					if nim[-i][-j]!=0 and nim[-i][-j+1]!=0:
						if nim[-i][-j]!=nim[-i][-j+1]:
							check=1
						nim[-i][-j]=min(nim[-i][-j],nim[-i][-j+1])
						
				elif j==1 and i>1:
					if nim[-i][-j]!=0 and nim[-i+1][-j]!=0:
						if nim[-i][-j]!=nim[-i+1][-j]:
							check=1
						nim[-i][-j]=min(nim[-i][-j],nim[-i+1][-j])
						
				elif j>1 and i>1:
					if nim[-i][-j]!=0 and nim[-i][-j+1]!=0:
						if nim[-i][-j]!=nim[-i][-j+1]:
							check=1
						nim[-i][-j]=min(nim[-i][-j],nim[-i][-j+1])
						
					if nim[-i][-j]!=0 and nim[-i+1][-j]!=0:
						if nim[-i][-j]!=nim[-i+1][-j]:
							check=1
						nim[-i][-j]=min(nim[-i][-j],nim[-i+1][-j])
						
	#print(nim[-1])
	#calculate area
	area=[]
	for i in range(row):
		for j in range(col):
			if nim[i][j]!=0:
				area.append(nim[i][j])
	#print(nim)
	for item in set(area):
		if area.count(item)>500:
			x=[]
			y=[]
			#print(x,y)
			for i in range(row):
				for j in range(col):
					if nim[i][j]==item:
						x.append(j)
						y.append(i)
			#print(min(x),min(y),max(x),max(y),item,area.count(item))
			print(min(x),min(y),max(x),max(y))
			cv.rectangle(im,(min(x),min(y)),(max(x),max(y)),(55,25,155),4)
			
	#for item in set(area):
	#	x=[]
	#	y=[]
			#print(x,y)
	#	for i in range(row):
	#		for j in range(col):
	#			if nim[i][j]==item:
	#				x.append(j)
	#				y.append(i)
	#	print(min(x),min(y),max(x),max(y),item,area.count(item))
		#cv.rectangle(nnim,(min(x),min(y)),(max(x),max(y)),(55,25,155),4)
			
	#print (nim)		
	#cv.nimwrite("connected.png",nnim)
	return nim
###	for item in set(area):
#		UL_x=999
#		UL_y=999
#		RD_x=0
#		RD_y=0
#		if area.count(item)>500:
#			for i in range(row):
#				for j in range(col):
#
#					if nim[i][j]==item and i<UL_y:
#						UL_y=i
#					if nim[i][j]==item and j<UL_x:
#						UL_x=j
#					if nim[i][j]==item and i>RD_y:
#						RD_y=i
#
#					if nim[i][j]==item and j>RD_x:
#						RD_x=j
###			print(UL_x,UL_y,RD_x,RD_y,item,area.count(item))
			#cv.rectangle(nim,(UL_x,UL_y),(RD_x,RD_y),(50,0,0),2)
#	cv.nimwrite("connected.png",nim)

	#return nimg
#rest=connected(test)   
rest=connected(img_gray)
#df=pd.DataFrame(rest)
#df.to_csv("IO.csv")
#cv.rectangle(nimg,(0,0),(512,512),(0,255,0),4)
#cv.rectangle(nimg,(100,317),(290,436),(0,255,0),4)
#cv.nimwrite("connected.png",nimg)
#print(connected(nimg_gray))
#cv.waitKey(0)

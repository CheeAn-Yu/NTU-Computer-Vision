import numpy as np
import cv2 as cv
import matplotlib.pyplot as plt
import pandas as pd
#np.set_printoptions(threshold=np.inf)
img=cv.imread("Lena.jpg")
#img_gray=cv.cvtColor(img, cv.COLOR_BGR2GRAY)#img_gray value can be stored always <256!!!!
img_gray=cv.imread("Lena.jpg",0)#0 for gray scale, 1 for color,-1 Unchanged

def bin (img):
	row=img.shape[0]
	col=img.shape[1]
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
	#print (x)
	for i in range(row):
		for j in range(col):
			p[img[i][j]]+=1
	plt.bar(x,p,align="center",alpha=0.5)
	plt.savefig("histogram.png")
	plt.show()
def findmin(label,r1,c1,r2,c2):
	if label[r2][c2]!=0:
		ans=min(label[r1][c1],label[r2][c2])
	else:
		ans=label[r1][c1]
	return ans
def connected(img):
	row=img.shape[0]
	col=img.shape[1]
	
	im=bin(img)
	nim=np.zeros((row,col),dtype=np.int)
	#df3=pd.DataFrame(nim)
	#df3.to_csv("binary.csv")

	label=1
	for i in range(row):
		for j in range(col):
			if im[i][j]==255:
				nim[i][j]=label
				label+=1
	
	#df2=pd.DataFrame(nim)
	#df2.to_csv("label.csv")
	check=1
	while check==1:
		check=0
		for i in range(row):#from left to right,up to down
			for j in range(col):
				temp=0
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
					if nim[i][j]!=0 :
						temp=findmin(nim,i,j,i-1,j)
						temp2=min(temp,nim[i][j-1])
						if temp2!=0:
							temp=temp2
						if nim[i][j]!=temp:
							check=1
						nim[i][j]=temp

								
				
		for i in range(1,row+1):
			for j in range(1,col+1):
				temp=0
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
					if nim[-i][-j]!=0:
						temp=findmin(nim,-i,-j,-i+1,-j)
						temp2=min(temp,nim[-i][-j+1])
						if temp2!=0:
							temp=temp2
						if nim[-i][-j]!=temp:
							check=1
						nim[-i][-j]=temp


						
	#print(im[-1])
	#calculate area
	area=[]
	for i in range(row):
		for j in range(col):
			if nim[i][j]!=0:
				area.append(nim[i][j])
	#print(im)
	rbg=cv.cvtColor(im, cv.COLOR_GRAY2BGR)
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
			print(min(x),min(y),max(x),max(y),item,area.count(item))
			
			cv.rectangle(rbg,(min(x),min(y)),(max(x),max(y)),(0,0,255),2)
	
	print (nim)		
	cv.imwrite("connected.png",rbg)
	return nim

rest=connected(img_gray)
df=pd.DataFrame(rest)
#df2=pd.DataFrame(label_im)
df.to_csv("IO.csv")
#df2.to_csv("label.csv")
#cv.rectangle(img,(0,0),(512,512),(0,255,0),4)
#cv.rectangle(img,(100,317),(290,436),(0,255,0),4)
#cv.imwrite("connected.png",img)
#print(connected(img_gray))
#cv.waitKey(0)

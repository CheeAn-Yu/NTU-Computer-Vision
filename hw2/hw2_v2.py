import numpy as np
import cv2 as cv
import matplotlib.pyplot as plt
#np.set_printoptions(threshold=np.inf)
img=cv.imread("lena512.bmp")
img_gray=cv.cvtColor(img, cv.COLOR_BGR2GRAY)
row=img.shape[0]
col=img.shape[1]
#test=np.array([[255,255,255,0,255,0],[0,0,255,0,255,0],[255,255,255,0,0,0],[0,255,0,255,0,0],[255,255,0,255,0,0]])
#test=np.array([[0,255,255,0,255,255,0,255],[0,255,255,0,255,255,0,255],[0,255,255,255,255,255,0,0]])
#test=np.array([[255,255,255,0,255,255,0,255],[0,0,255,0,255,255,0,255],[255,255,255,0,255,255,0,255]])
#test=np.array([[255,255,255,0,255,255,0,255],[0,0,255,0,255,255,0,255],[255,255,255,0,255,255,255,255]])
#print (img[0][0],img[-512][-512])

def bin (img):
	row=img.shape[0]
	col=img.shape[1]
	for i in range(row):
		for j in range(col):
			new=img.copy()
			if img[i][j]<128:
				new[i][j]=0
			else:
				new[i][j]=255
    
	#cv.imwrite("thresold_128.png",img)
	return new
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
	row=img.shape[0]
	col=img.shape[1]
	for i in range(row):
		for j in range(col):
			if im[i][j]==255:
				im[i][j]=label
				label+=1
	check=1
	while check==1:
		check=0
		for i in range(row):#from left to right,up to down
			for j in range(col):

				if i==0 and j-1>=0:
					if im[i][j]!=0 and im[i][j-1]!=0:
						if im[i][j]!=im[i][j-1]:
							check=1
						im[i][j]=min(im[i][j],im[i][j-1])
						
				if j==0 and i-1>=0:
					if im[i][j]!=0 and im[i-1][j]!=0:
						if im[i][j]!=im[i-1][j]:
							check=1
						im[i][j]=min(im[i][j],im[i-1][j])
						
				elif i>0 and j>0:
					if im[i][j]!=0 and (im[i-1][j]!=0 or im[i][j-1]!=0):
						if im[i-1][j]!=0 and im[i][j-1]!=0:
							
							im[i][j]=min(im[i][j],im[i-1][j],im[i][j-1])
						elif im[i-1][j]!=0 and im[i][j-1]==0:
							im[i][j]=min(im[i][j],im[i-1][j])
						elif im[i][j-1]!=0 and im[i-1][j]==0:
							im[i][j]=min(im[i][j],im[i][j-1])	
			
				
		for i in range(1,row+1):
			for j in range(1,col+1):
				if i==1 and j>1:
					if im[-i][-j]!=0 and im[-i][-j+1]!=0:
						if im[-i][-j]!=im[-i][-j+1]:
							check=1
						im[-i][-j]=min(im[-i][-j],im[-i][-j+1])
						
				if j==1 and i>1:
					if im[-i][-j]!=0 and im[-i+1][-j]!=0:
						if im[-i][-j]!=im[-i+1][-j]:
							check=1
						im[-i][-j]=min(im[-i][-j],im[-i+1][-j])
						
				elif j>1 and i>1:
					if im[-i][-j]!=0 and (im[-i][-j+1]!=0 or im[-i+1][-j]!=0):
						if im[-i][-j+1]!=0 and im[-i+1][-j]!=0:
							im[-i][-j]=min(im[-i][-j],im[-i][-j+1],im[-i+1][-j])
						elif im[-i][-j+1]==0:
							im[-i][-j]=min(im[-i][-j],im[-i+1][-j])
						elif im[-i+1][-j]==0:
							im[-i][-j]=min(im[-i][-j],im[-i][-j+1])
						
					
						
	#print(im[-1])
	#calculate area
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
###	for item in set(area):
#		UL_x=999
#		UL_y=999
#		RD_x=0
#		RD_y=0
#		if area.count(item)>500:
#			for i in range(row):
#				for j in range(col):
#
#					if im[i][j]==item and i<UL_y:
#						UL_y=i
#					if im[i][j]==item and j<UL_x:
#						UL_x=j
#					if im[i][j]==item and i>RD_y:
#						RD_y=i
#
#					if im[i][j]==item and j>RD_x:
#						RD_x=j
###			print(UL_x,UL_y,RD_x,RD_y,item,area.count(item))
			#cv.rectangle(im,(UL_x,UL_y),(RD_x,RD_y),(50,0,0),2)
#	cv.imwrite("connected.png",im)

	#return img
#print(test)   
#rest=connected(test)
rest=connected(img_gray)
#cv.rectangle(img,(0,0),(512,512),(0,255,0),4)
#cv.rectangle(img,(100,317),(290,436),(0,255,0),4)
#cv.imwrite("connected.png",img)
#print(connected(img_gray))
#cv.waitKey(0)

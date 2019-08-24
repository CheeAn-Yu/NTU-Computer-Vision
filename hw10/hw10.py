import numpy as np
import cv2
import math
import pandas as pd
img_ori = cv2.imread('lena.bmp',0)

def Laplacian1(img, threshold):
	row,col=img.shape
	new=np.zeros(shape=(row,col))
	res=np.zeros(shape=(row,col))
	mask=[[0,1,0],[1,-4,1],[0,1,0]]
	for i in range(row):
		for j in range(col):
			s1=0
			for X in range(-1,2):
				for Y in range(-1,2):
					if X+i>=0 and X+i<row and j+Y>=0 and j+Y<col:
						s1+=mask[X+1][Y+1]*img[i+X][j+Y]
			new[i][j]=s1
	for i in range(row):
		for j in range(col):
			if new[i][j]>threshold:
				for X in range(-1,2):
					for Y in range(-1,2):
						if X+i>=0 and X+i<row and j+Y>=0 and j+Y<col:
							if new[i+X][j+Y]<-1*threshold:
								res[i][j]=255

			#if s1>threshold:
			#	res[i][j]=255
	return res

def Laplacian2(img,threshold):
	row,col=img.shape
	new=np.zeros(shape=(row,col))
	res=np.zeros(shape=(row,col))
	mask=[[1.0/3,1.0/3,1.0/3],[1.0/3,-8.0/3,1.0/3],[1.0/3,1.0/3,1.0/3]]
	for i in range(row):
		for j in range(col):
			s1=0.0
			for X in range(-1,2):
				for Y in range(-1,2):
					if X+i>=0 and X+i<row and j+Y>=0 and j+Y<col:
						s1+=mask[X+1][Y+1]*img[i+X][j+Y]
			new[i][j]=s1
	for i in range(row):
		for j in range(col):
			if new[i][j]>threshold:
				for X in range(-1,2):
					for Y in range(-1,2):
						if new[i+X][j+Y]<-1*threshold:
							res[i][j]=255
	return res

def mini_variance(img,threshold):
	row,col=img.shape
	new=np.zeros(shape=(row,col))
	res=np.zeros(shape=(row,col))
	mask=[[2.0/3,-1.0/3,2.0/3],[-1.0/3,-4.0/3,-1.0/3],[2.0/3,-1.0/3,2.0/3]]
	for i in range(row):
		for j in range(col):
			s1=0.0
			for X in range(-1,2):
				for Y in range(-1,2):
					if X+i>=0 and X+i<row and j+Y>=0 and j+Y<col:
						s1+=mask[X+1][Y+1]*img[i+X][j+Y]
			new[i][j]=s1
	for i in range(row):
		for j in range(col):
			if new[i][j]>threshold:
				for X in range(-1,2):
					for Y in range(-1,2):
						if X+i>=0 and X+i<row and j+Y>=0 and j+Y<col:
							if new[i+X][j+Y]<-1*threshold:
								res[i][j]=255
	return res

def Laplace_Gaussion(img,threshold):
	row,col=img.shape
	new=np.zeros(shape=(row,col))
	res=np.zeros(shape=(row,col))
	mask=[[0,0,0,-1,-1,-2,-1,-1,0,0,0],
		  [0,0,-2,-4,-8,-9,-8,-4,-2,0,0],
		  [0,-2,-7,-15,-22,-23,-22,-15,-7,-2,0],
		  [-1,-4,-15,-24,-14,-1,-14,-24,-15,-4,-1],
		  [-1,-8,-22,-14,52,103,52,-14,-22,-8,-1],
		  [-2,-9,-23,-1,103,178,103,-1,-23,-9,-2],
		  [-1,-8,-22,-14,52,103,52,-14,-22,-8,-1],
		  [-1,-4,-15,-24,-14,-1,-14,-24,-15,-4,-1],
		  [0,-2,-7,-15,-22,-23,-22,-15,-7,-2,0],
		  [0,0,-2,-4,-8,-9,-8,-4,-2,0,0],
		  [0,0,0,-1,-1,-2,-1,-1,0,0,0]]
	for i in range(row):
		for j in range(col):
			s1=0.0
			for X in range(-5,6):
				for Y in range(-5,6):
					if X+i>=0 and X+i<row and j+Y>=0 and j+Y<col:
						s1+=mask[X+5][Y+5]*img[i+X][j+Y]
			new[i][j]=s1
	for i in range(row):
		for j in range(col):
			if new[i][j]>threshold:
				for X in range(-1,2):
					for Y in range(-1,2):
						if X+i>=0 and X+i<row and j+Y>=0 and j+Y<col:
							if new[i+X][j+Y]<-1*threshold:
								res[i][j]=255
	return res
def Difference_Gaussion(img,threshold):
	row,col=img.shape
	new=np.zeros(shape=(row,col))
	res=np.zeros(shape=(row,col))
	mask=np.zeros(shape=(11,11))
	sigma1=1
	sigma2=3
	mean=0
	for i in range(-5,6):
		for j in range(-5,6):
			a=math.exp( -(i**2+j**2)/(2.0*sigma1*sigma1) )/ (math.sqrt(2*math.pi)*sigma1)
			b=math.exp( -(i**2+j**2)/(2.0*sigma2*sigma2) )/ (math.sqrt(2*math.pi)*sigma2)
			mask[i+5][j+5]=a-b
			mean+=a-b
	mean/=11*11
	for i in range(11):
		for j in range(11):
			mask[i][j]-=mean

	for i in range(row):
		for j in range(col):
			s1=0.0
			for X in range(-5,6):
				for Y in range(-5,6):
					if X+i>=0 and X+i<row and j+Y>=0 and j+Y<col:
						s1+=mask[X+5][Y+5]*img[i+X][j+Y]
						#print(X,Y,i,j)
			new[i][j]=s1
	for i in range(row):
		for j in range(col):
			if new[i][j]>threshold:
				for X in range(-1,2):
					for Y in range(-1,2):
						if X+i>=0 and X+i<row and j+Y>=0 and j+Y<col:
							if new[i+X][j+Y]<-1*threshold:
								res[i][j]=255
	return res


#L1=Laplacian1(img_ori,20)
#cv2.imwrite("Laplacian1_20.jpg",L1)
#L2=Laplacian2(img_ori,18)
#cv2.imwrite("Laplacian2_18.jpg",L2)
#mini=mini_variance(img_ori,15)
#cv2.imwrite("mini_variance_15.jpg",mini)
#LG=Laplace_Gaussion(img_ori,1300)
#cv2.imwrite("Laplace_Gaussion_1300.jpg",LG)
DG=Difference_Gaussion(img_ori,4)
cv2.imwrite("Difference_Gaussion_4.jpg",DG)
"""
mask=np.zeros(shape=(11,11))
sigma1=1
sigma2=3
mean=0
for i in range(-5,6):
	for j in range(-5,6):
		a=math.exp( -(i**2+j**2)/(2.0*sigma1*sigma1) )/ (math.sqrt(2*math.pi)*sigma1)
		b=math.exp( -(i**2+j**2)/(2.0*sigma2*sigma2) )/ (math.sqrt(2*math.pi)*sigma2)
		#print(a,b)
		mask[i+5][j+5]=a-b
		mean+=a-b
mean/=11*11
for i in range(11):
	for j in range(11):
		mask[i][j]-=mean
print(mask,mean)
df=pd.DataFrame(mask)
df.to_csv("mask.csv")"""
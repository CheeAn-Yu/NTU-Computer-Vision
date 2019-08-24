import cv2
import pandas as pd
import numpy as np
img=cv2.imread("Lena.jpg",0)


def downside(img):
	row=img.shape[0]
	col=img.shape[1]
	res=np.zeros((row/8,col/8), dtype=np.int)
	for i in range(0,row,8):
		for j in range(0,col,8):
			res[i/8][j/8]=img[i][j]
	return res
def bin(img):
	row,col=img.shape
	res=np.zeros((row,col), dtype=np.int)
	for i in range(row):
		for j in range(col):
			if img[i][j]>128:
				res[i][j]=255
			else: 
				res[i][j]=0
	return res
def h(c,d):
	if c==d:
		return "c"
	elif c!=d:
		return "b"
def f(c):
	if c=="b":
		return "b"
	elif c!= "b":
		return "i"

def IB(img):
	row,col=img.shape
	new=[[" "for i in range(66)] for i in range(66)]
	res=[[" "for i in range(66)] for i in range(66)]
	#new=np.zeros((row+2,col+2),dtype=np.int)
	#res=np.zeros((row+2,col+2),dtype=np.int)
	rsize=np.zeros((row,col),dtype=np.int)
	fres=[[" "for i in range(64)] for i in range(64)]
	for i in range(row):
		for j in range(col):
			if img[i][j]==255:
				new[i+1][j+1]=img[i][j]
	for i in range(1,row+1):
		for j in range(1,col+1):	
			if new[i][j]==255:
				a0=new[i][j]
				a1=h(a0,new[i][j+1])
				a2=h(a1,new[i-1][j])
				a3=h(a2,new[i][j-1])
				a4=h(a3,new[i+1][j])
				new[i][j]=f(a4)
	for i in range(row):
		for j in range(col):
			fres[i][j]=res[i+1][j+1]

	return fres			
#def PairRelation(i,j,img):
#	if img[i][j]==1 and (img[i][j+1]+img[i-1][j]+img[i][j-1]+img[i+1][j]

bi=bin(img)
ds=downside(bi)
yk=yokoi(ds)
#print(yk)
df=pd.DataFrame(yk)
df.to_csv("hw6.csv")
df=pd.DataFrame(ds)
df.to_csv("ds.csv")
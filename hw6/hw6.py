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
def h(b,c,d,e):
	if b==c and ((d != b) or (e != b)):
		return "q"
	elif b==c and ((d==b) and (e==b)):
		return "r"
	elif b != c:
		return "s"
def f(a1,a2,a3,a4):
	if a1==a2 and a1==a3 and a1==a4 and a1=="r":
		return 5
	else:
		l=[a1,a2,a3,a4]
		#print(l)
		count=l.count("q")
		return count

def yokoi(img):
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
				l=[]
				l.append(h(new[i][j],new[i][j+1],new[i-1][j+1],new[i-1][j]))
				l.append(h(new[i][j],new[i-1][j],new[i-1][j-1],new[i][j-1]))
				l.append(h(new[i][j],new[i][j-1],new[i+1][j-1],new[i+1][j]))
				l.append(h(new[i][j],new[i+1][j],new[i+1][j+1],new[i][j+1]))
				res[i][j]=f(l[0],l[1],l[2],l[3])
	for i in range(row):
		for j in range(col):
			fres[i][j]=res[i+1][j+1]

	return fres			


bi=bin(img)
ds=downside(bi)
yk=yokoi(ds)
#print(yk)
df=pd.DataFrame(yk)
df.to_csv("hw6.csv")
df=pd.DataFrame(ds)
df.to_csv("ds.csv")
import cv2
import pandas as pd
import numpy as np
img=cv2.imread("Lena.jpg",0)



def downside(img):
	row=img.shape[0]
	col=img.shape[1]
	res=[[0 for i in range(row/8)]for j in range(col/8)]
	#res=np.zeros((row/8,col/8), dtype=np.int)
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
		return 255
	elif c!=d:
		return 0
def I(a,i):
	if a=="i":
		return 1
	else:
		return 0
def f(c):
	if c==0:
		return "b"
	elif c!=0:
		return "i"

def IB(img):#thinning
	#row,col=img.shape
	row=len(img)
	col=len(img)
	new=[[" "for i in range(row+2)] for i in range(col+2)]
	res=[[" "for i in range(row+2)] for i in range(col+2)]
	fres=[[" "for i in range(row)] for i in range(col)]
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
				
				res[i][j]=f(a4)
				

	for i in range(row):
		for j in range(col):
			fres[i][j]=res[i+1][j+1]


	return fres			
#def PairRelation(i,j,img):
#	if I(img[i][j+1],"i")+I(img[i-1][j],"i")+I(img[i][j-1],"i")+I(img[i+1][j],"i")<1 or img[i][j]!="b":
		#print(I(img[i][j+1],"i")+I(img[i-1][j],"i")+I(img[i][j-1],"i")+I(img[i+1][j],"i"))
#		return "q"
#	elif I(img[i][j+1],"i")+I(img[i-1][j],"i")+I(img[i][j-1],"i")+I(img[i+1][j],"i")>=1 and img[i][j]=="b":
#		return "p"
def PR(img):
	row=len(img)
	col=len(img)
	#print(row,col)
	new=[[" "for i in range(row+2)] for i in range(col+2)]
	res=[[" "for i in range(row+2)] for i in range(col+2)]
	fres=[[" "for i in range(row)] for i in range(col)]
	for i in range(row):
		for j in range(col):
			if img[i][j]=="b" or img[i][j]=="i":
				new[i+1][j+1]=img[i][j]
	
	for i in range(1,row+1):
		for j in range(1,col+1):
			if new[i][j]=="b" and((new[i][j+1]=="b"or new[i-1][j]=="b" or new[i][j-1]=="b" or new[i+1][j]=="b")):
				res[i][j]="p"
			else:
				res[i][j]="q"
				
	for i in range(row):
		for j in range(col):
			fres[i][j]=res[i+1][j+1]
	return fres
def removeable(i,j,new):
	def h(b,c,d,e):
		if b==c and ((d != b) or (e != b)):
			return 1
		else:
			return 0

	l=[]
	l.append(h(new[i][j],new[i][j+1],new[i-1][j+1],new[i-1][j]))
	l.append(h(new[i][j],new[i-1][j],new[i-1][j-1],new[i][j-1]))
	l.append(h(new[i][j],new[i][j-1],new[i+1][j-1],new[i+1][j]))
	l.append(h(new[i][j],new[i+1][j],new[i+1][j+1],new[i][j+1]))
	res=sum(l)
	if res==1:
		return True
def thinning(img):
	row=len(img)
	col=len(img)
	#print(row,col,"fuck")
	ib=IB(img)
	pr=PR(ib)
	new=[[" "for i in range(row+2)] for i in range(col+2)]
	res=[[" "for i in range(row+2)] for i in range(col+2)]
	fres=[[0 for i in range(row)] for i in range(col)]

	for i in range(row):
		for j in range(col):
			if img[i][j]==255:
				new[i+1][j+1]=img[i][j]
				res[i+1][j+1]=img[i][j]
				fres[i][j]=img[i][j]
	for i in range(1,row):
		for j in range(1,col):
			if pr[i-1][j-1]=="p" and removeable(i,j,new):
				res[i][j]=0
	for i in range(row):
		for j in range(col):
			if res[i+1][j+1]==0:
				fres[i][j]=res[i+1][j+1]
	return fres
def same(img1,img2):
	for i in range(len(img1)):
		for j in range(len(img1)):
			if img1[i][j]!=img2[i][j]:
				return False
			
	return True
def test(a):
	return a+[1,1]
def main():
	bi=bin(img)
	ds=downside(bi)#255
	yk=IB(ds)#interior border
	pr=PR(yk)#qp
	count=0
	check=True
	while(check):
		th=thinning(ds)
		if same(th,ds)==0:
			ds=th
			count+=1
			cv2.imwrite("th"+str(count)+".jpg",np.asarray(ds))
		else:
			check=False
		#for i in range (len(ds)):
		#	for j in range(len(ds)):
		#		if th[i][j]!=ds[i][j]:
		#			count+=1
		#			for k in range(len(ds)):
		#				for l in range(len(ds)):
		#					ds[k][l]=th[k][l]
		#print(th,"th")
		#print(ds,"ds")
	print(count)
	new=np.zeros((64,64),dtype=np.int)
	for i in range(64):
		for j in range(64):
			if th[i][j]==255:
				new[i][j]=255

	#np.asarray(th)
	cv2.imwrite("thinning.jpg",new)
	df1=pd.DataFrame(th)
	df1.to_csv("hw7.csv")


	


main()



#bi=bin(img)
#ds=downside(bi)#255
#yk=IB(ds)#interior border
#pr=PR(yk)#qp
#th=thinning(ds)

#df=pd.DataFrame(yk)
#df.to_csv("IB.csv")
#df=pd.DataFrame(ds)
#df.to_csv("ds.csv")
#df=pd.DataFrame(pr)
#df.to_csv("PR.csv")
#df=pd.DataFrame(th)
#df.to_csv("hw7.csv")
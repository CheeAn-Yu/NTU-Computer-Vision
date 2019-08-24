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


def yokoi(img):
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
	row=len(img[0])
	col=len(img[1])
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
#def PairRelation(i,j,img):
#	if I(img[i][j+1],"i")+I(img[i-1][j],"i")+I(img[i][j-1],"i")+I(img[i+1][j],"i")<1 or img[i][j]!="b":
#		#print(I(img[i][j+1],"i")+I(img[i-1][j],"i")+I(img[i][j-1],"i")+I(img[i+1][j],"i"))
#		return "q"
#	elif I(img[i][j+1],"i")+I(img[i-1][j],"i")+I(img[i][j-1],"i")+I(img[i+1][j],"i")>=1 and img[i][j]=="b":
#		return "p"
def PairRelation(img):
	row=len(img)
	col=len(img)
	#print(row,col)
	new=[[" "for i in range(row+2)] for i in range(col+2)]
	res=[[" "for i in range(row+2)] for i in range(col+2)]
	fres=[[" "for i in range(row)] for i in range(col)]
	for i in range(row):
		for j in range(col):
			if img[i][j]!=" ":
				new[i+1][j+1]=img[i][j]
	
	for i in range(1,row+1):
		for j in range(1,col+1):
			if new[i][j]==1 and(new[i][j+1]==1 or new[i-1][j]==1 or new[i][j-1] or new[i+1][j]==1):
				res[i][j]="p"
			elif new[i][j]!=1 and new[i][j]!=" ":
				res[i][j]="q"

	for i in range(row):
		for j in range(col):
			fres[i][j]=res[i+1][j+1]
	return fres
def removeable(i,j,new):
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
	l=[]
	l.append(h(new[i][j],new[i][j+1],new[i-1][j+1],new[i-1][j]))
	l.append(h(new[i][j],new[i-1][j],new[i-1][j-1],new[i][j-1]))
	l.append(h(new[i][j],new[i][j-1],new[i+1][j-1],new[i+1][j]))
	l.append(h(new[i][j],new[i+1][j],new[i+1][j+1],new[i][j+1]))
	res=f(l[0],l[1],l[2],l[3])
	if res==1:
		return True
def thinning(img):
	row=len(img)
	col=len(img)
	#print(row,col,"fuck")
	new=[[0  for i in range(row+2)] for i in range(col+2)]
	res=[[0 for i in range(row+2)] for i in range(col+2)]
	fres=[[0 for i in range(row)] for i in range(col)]

	ib=yokoi(img)
	pr=PairRelation(ib)

	for i in range(row):
		for j in range(col):
			if img[i][j]==255:
				new[i+1][j+1]=img[i][j]
				res[i+1][j+1]=img[i][j]
	for i in range(1,row+1):
		for j in range(1,col+1):
			if pr[i-1][j-1]=="p":
				if removeable(i,j,new):
					new[i][j]=0
	for i in range(row):
		for j in range(col):
			if new[i+1][j+1]==255:
				fres[i][j]=new[i+1][j+1]
	return fres
def same(img1,img2):
	for i in range(len(img1)):
		for j in range(len(img1)):
			if img1[i][j]!=img2[i][j]:
				return False
			
	return True
def main():
	bi=bin(img)
	ds=downside(bi)#255
	yk=yokoi(ds)#interior border
	df=pd.DataFrame(yk)
	df.to_csv("yk.csv")
	pr=PairRelation(yk)#qp
	df=pd.DataFrame(pr)
	df.to_csv("pr.csv")
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
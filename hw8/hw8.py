import cv2
import pandas as pd
import numpy as np
import math
img1=cv2.imread("Lena.jpg",0)
x,y = img1.shape
#def Gaussian_noise(img,amp):
#	row=img.shape[0]
#	col=img.shape[1]
#	new=np.zeros((row,col),dtype=np.uint8)
#	for i in range(row):
#		for j in range(col):
#			new[i][j]=img[i][j]+amp*np.random.normal(0,1)
	
#	return new
def Gaussian_noise(img,amp):
    return img+amp*np.random.normal(0,1,(x,y))

def SP_noise(img,threshold):
	row,col=img.shape
	new=np.zeros(shape=(row,col))
	for i in range(row):
		for j in range(col):
			if np.random.uniform(0,1)<threshold:
				new[i][j]=0
			elif np.random.uniform(0,1)>1-threshold:
				new[i][j]=255
			else:
				new[i][j]=img[i][j]
	return new

def box_filter3x3(img):
	row,col=img.shape
	new=np.zeros(shape=(row+2,col+2))
	res=np.zeros(shape=(row+2,col+2))
	fres=np.zeros(shape=(row,col))
	for i in range(row):
		for j in range(col):
			new[i+1][j+1]=img[i][j]
	box=[(0,0),(0,1),(0,-1),(-1,-1),(-1,0),(-1,1),(1,-1),(1,0),(1,1)]
	for i in range(1,row+1):
		for j in range(1,col+1):
			s=0
			for m,n in box:
				#print(i+m,j+n)
				s+=new[i+m][j+n]
			res[i][j]=s/9
	for i in range(row):
		for j in range(col):
			fres[i][j]=res[i+1][j+1]
	return fres
def box_filter5x5(img):
	row,col=img.shape
	new=np.zeros(shape=(row+4,col+4))
	res=np.zeros(shape=(row+4,col+4))
	fres=np.zeros(shape=(row,col))
	for i in range(row):
		for j in range(col):
			new[i+2][j+2]=img[i][j]
	box=[]
	for i in range(-2,3):
		for j in range(-2,3):
			box.append((i,j))
	#print box
	#box=[(0,0),(0,1),(0,-1),(0,2),(0,-2),(-1,-2),(-1,-1),(-1,0),(-1,1),(1,-1),(1,0),(1,1)]
	for i in range(2,row+2):
		for j in range(2,col+2):
			s=0
			for m,n in box:
				#print(i+m,j+n)
				s+=new[i+m][j+n]
			res[i][j]=s/25

	for i in range(row):
		for j in range(col):
			fres[i][j]=res[i+2][j+2]
	return fres
def median_filter3x3(img):
	row,col=img.shape
	new=np.zeros(shape=(row+2,col+2))
	res=np.zeros(shape=(row+2,col+2))
	fres=np.zeros(shape=(row,col))
	for i in range(row):
		for j in range(col):
			new[i+1][j+1]=img[i][j]
	box=[(0,0),(0,1),(0,-1),(-1,-1),(-1,0),(-1,1),(1,-1),(1,0),(1,1)]
	for i in range(1,row+1):
		for j in range(1,col+1):
			s=[]
			for m,n in box:
				s.append(new[i+m][j+n])
			s.sort()
			res[i+1][j+1]=s[4]
	for i in range(row):
		for j in range(col):
			fres[i][j]=res[i+1][j+1]
	return fres
def median_filter5x5(img):
	row,col=img.shape
	new=np.zeros(shape=(row+4,col+4))
	res=np.zeros(shape=(row+4,col+4))
	fres=np.zeros(shape=(row,col))
	for i in range(row):
		for j in range(col):
			new[i+2][j+2]=img[i][j]
	box=[]
	for i in range(-2,3):
		for j in range(-2,3):
			box.append((i,j))

	for i in range(2,row+2):
		for j in range(2,col+2):
			s=[]
			for m,n in box:
				s.append(new[i+m][j+n])
			s.sort()
			res[i][j]=s[12]
	for i in range(row):
		for j in range(col):
			fres[i][j]=res[i+2][j+2]
	return fres


def dilation(img):
	def dil_kernal(img,row,col):
		value=[]
		for i in range(-2,3):
			for j in range(-2,3):
				if (i==-2 and j==-2) or (i==-2 and j==2)or(i==2 and j==-2)or(i==2 and j==2):
					pass
				else:
					value.append(img[row+i][col+j])
		return max(value)
	row=img.shape[0]
	col=img.shape[1]
	new=np.zeros((row+4,col+4),dtype=np.int)
	res=np.zeros((row,col),dtype=np.int)

	for i in range(row):
		for j in range(col):
			new[i+2][j+2]=img[i][j]

	for i in range(row):
		for j in range(col):
			res[i][j]=dil_kernal(new,i+2,j+2)
	return res
def erosion(img):
	def ero_kernal(img,row,col):
		value=[]
		for i in range(-2,3):
			for j in range(-2,3):
				if (i==-2 and j==-2) or (i==-2 and j==2)or(i==2 and j==-2)or(i==2 and j==2):
					pass
				else:
					value.append(img[row+i][col+j])
					
		return min(value)
	row=img.shape[0]
	col=img.shape[1]
	new=np.zeros((row+4,col+4),dtype=np.int)
	res=np.zeros((row,col),dtype=np.int)
	for i in range(row):
		for j in range(col):
			new[i+2][j+2]=img[i][j]

	for i in range(row):
		for j in range(col):
				res[i][j]=ero_kernal(new,i+2,j+2)
	return res		
def opening(img):
	ero_im=erosion(img)
	open_im=dilation(ero_im)
	return open_im
def closing(img):
	dil_im=dilation(img)
	close_im=erosion(dil_im)
	return close_im
def OC_filter(img):
	op=opening(img)
	cl=closing(op)
	return cl
def CO_filter(img):
	cl=closing(img)
	op=opening(cl)
	return op
def SNR(c1,n2):
	row,col=c1.shape
	cs=0
	ns=0
	for i in range(row):
		for j in range(col):
			cs+=c1[i][j]
			ns+=(n2[i][j]-c1[i][j])
	ms=cs/(row*col)
	mn=ns/(row*col)
	#print(ms,mn)
	VS=0
	VN=0
	for i in range(row):
		for j in range(col):
			VS+=(c1[i][j]-ms)**2
			VN+=(n2[i][j]-c1[i][j]-mn)**2
	#print(VS,VN)
	VS=VS/(row*col)
	VN=VN/(row*col)

	#print(VS,VN)
	ans=20*math.log10((VS**0.5)/(VN**0.5))
	return ans








gn10=Gaussian_noise(img1,10)
gn30=Gaussian_noise(img1,30)
sp05=SP_noise(img1,0.05)
sp01=SP_noise(img1,0.1)

#cv2.imwrite("Gaussian_noise10.jpg",gn10)
#cv2.imwrite("Gaussian_noise30.jpg",gn30)
#cv2.imwrite("SP005.jpg",sp05)
#cv2.imwrite("SP01.jpg",sp01)
#print(SN(img,Gb3))

#Gb5=box_filter5x5(gn10)
#cv2.imwrite("box5x5_gn10.jpg",Gb5)
#box3_gn10=box_filter3x3(gn10)
#box3_gn30=box_filter3x3(gn30)
#box3_sp05=box_filter3x3(sp05)
#box3_sp01=box_filter3x3(sp01)
#cv2.imwrite("box3x3_gn10.jpg",box3_gn10)
#cv2.imwrite("box3x3_gn30.jpg",box3_gn30)
#cv2.imwrite("box3x3_sp005.jpg",box3_sp05)
#cv2.imwrite("box3x3_sp01.jpg",box3_sp01)
#print(SNR(img1,box3_gn10))
#print(SNR(img1,box3_gn30))
#print(SNR(img1,box3_sp05))
#print(SNR(img1,box3_sp01))
#box5_gn10=box_filter5x5(gn10)
#box5_gn30=box_filter5x5(gn30)
#box5_sp05=box_filter5x5(sp05)
#box5_sp01=box_filter5x5(sp01)
#cv2.imwrite("box5x5_gn10.jpg",box5_gn10)
#cv2.imwrite("box5x5_gn30.jpg",box5_gn30)
#cv2.imwrite("box5x5_sp005.jpg",box5_sp05)
#cv2.imwrite("box5x5_sp01.jpg",box5_sp01)


#med_Gn10=median_filter3x3(gn10)
#med_Gn30=median_filter3x3(gn30)
#med_sp05=median_filter3x3(sp05)
#med_sp01=median_filter3x3(sp01)
#cv2.imwrite("med_Gn30.jpg",med_Gn30)
#cv2.imwrite("med_Gn10.jpg",med_Gn10)
#cv2.imwrite("med3x3_sp05.jpg",sp05)
#cv2.imwrite("med3x3_sp01.jpg",sp01)

#med5x5=median_filter5x5(gn10)
#cv2.imwrite("med5x5_gn10.jpg",med5x5)
#med5x5_sp01=median_filter5x5(sp01)
#cv2.imwrite("med5x5_sp01.jpg",med5x5_sp01)
#med5_gn30=median_filter5x5(gn30)
#med5_sp05=median_filter5x5(sp05)
#cv2.imwrite("med5x5_gn30.jpg",med5_gn30)
#cv2.imwrite("med5x5_sp05.jpg",med5_sp05)



#ocg10=OC_filter(gn10)
#ocg30=OC_filter(gn30)
#cv2.imwrite("opening_closing_gn30.jpg",ocg30)
#ocsp05=OC_filter(sp05)
#cv2.imwrite("opening_closing_sp05.jpg",ocsp05)
#ocsp01=OC_filter(sp01)
#cv2.imwrite("opening_closoing_sp01.jpg",ocsp01)
#cv2.imwrite("opening_closing_gn10.jpg",ocg10)


co=CO_filter(gn10)
cv2.imwrite("closing_opening_gn10.jpg",co)
co_gn30=CO_filter(gn30)
co_sp01=CO_filter(sp01)
co_sp05=CO_filter(sp05)
cv2.imwrite("closing_opening_gn30.jpg",co_gn30)
cv2.imwrite("closing_opening_sp01.jpg",co_sp01)
cv2.imwrite("closing_opening_sp05.jpg",co_sp05)
print(SNR(img1,co))
print(SNR(img1,co_gn30))
print(SNR(img1,co_sp05))
print(SNR(img1,co_sp01))

#cv2.imshow("Gaussian_noise",np.array(gn30, dtype=np.uint8))
#cv2.imwrite("Gaussian_noise30.jpg",gn30)
#cv2.waitKey(0)
#print(gn30)

#noise=np.random.normal(0,1,(3,3))
#print(noise)
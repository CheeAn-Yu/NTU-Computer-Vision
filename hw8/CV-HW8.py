import numpy as np
import cv2
import math
import pandas as pd
img_ori = cv2.imread('Lena.jpg',cv2.IMREAD_GRAYSCALE)
x,y = img_ori.shape

def Gaussian_noise(img,amp):
    return img+amp*np.random.normal(0,1,(x,y))

def Salt_and_pepper_noise(img,threshold):
    ret=np.random.uniform(0,1,(x,y))
    for i in range (x):
        for j in range (y):
            value=ret[i,j]
            if value<threshold:
                ret[i,j]=0
            elif value>1-threshold:
                ret[i,j]=255
            else:
                ret[i,j]=img[i,j]
    return ret

img_Gau10=Gaussian_noise(img_ori,10)
img_Gau30=Gaussian_noise(img_ori,30)
img_Salt005=Salt_and_pepper_noise(img_ori,0.05)
img_Salt01=Salt_and_pepper_noise(img_ori,0.1)

def box_filter_3x3(img):
    ret=np.zeros(shape=(x,y))
    for i in range (x):
        for j in range (y):
            box=[]
            for X in range (-1,2):
                for Y in range (-1,2):
                    if i+X>=0 and i+X<x and j+Y>=0 and j+Y<y:
                        box.append(img[i+X,j+Y])
            ret[i,j]=sum(box)/len(box)
    return ret
    
def box_filter_5x5(img):
    ret=np.zeros(shape=(x,y))
    for i in range (x):
        for j in range (y):
            box=[]
            for X in range (-2,3):
                for Y in range (-2,3):
                    if i+X>=0 and i+X<x and j+Y>=0 and j+Y<y:
                        box.append(img[i+X,j+Y])
            ret[i,j]=sum(box)/len(box)
    return ret
    
def median_filter_3x3(img):
    ret=np.zeros(shape=(x,y))
    for i in range (x):
        for j in range (y):
            box=[]
            for X in range (-1,2):
                for Y in range (-1,2):
                    if i+X>=0 and i+X<x and j+Y>=0 and j+Y<y:
                        box.append(img[i+X,j+Y])
            box.sort()
            n=len(box)
            if n%2==1:
                ret[i,j]=box[int((n-1)/2)]
            else:
                ret[i,j]=(box[int(n/2)]+box[int(n/2-1)])/2
    return ret
    
def median_filter_5x5(img):
    ret=np.zeros(shape=(x,y))
    for i in range (x):
        for j in range (y):
            box=[]
            for X in range (-2,3):
                for Y in range (-2,3):
                    if i+X>=0 and i+X<x and j+Y>=0 and j+Y<y:
                        box.append(img[i+X,j+Y])
            box.sort()
            n=len(box)
            if n%2==1:
                ret[i,j]=box[int((n-1)/2)]
            else:
                ret[i,j]=(box[int(n/2)]+box[int(n/2-1)])/2
    return ret

def Dilation(img):
    ret=np.zeros(shape=(x,y))
    for i in range (x):
        for j in range (y):
            if img[i,j]!=0:
                box=[]
                for X in range (-2,3):
                    for Y in range (-2,3):
                        if (X,Y)!=(-2,-2) and (X,Y)!=(-2,2) and (X,Y)!=(2,2) and (X,Y)!=(2,-2):
                            if i+X>=0 and i+X<x and j+Y>=0 and j+Y<y:
                                box.append(img[i+X,j+Y])
                ret[i,j]=max(box)
    return ret
    
def Erosion(img):
    ret=np.zeros(shape=(x,y))
    for i in range (x):
        for j in range (y):
            box=[]
            for X in range (-2,3):
                for Y in range (-2,3):
                    if (X,Y)!=(-2,-2) and (X,Y)!=(-2,2) and (X,Y)!=(2,2) and (X,Y)!=(2,-2):
                        if i+X>=0 and i+X<x and j+Y>=0 and j+Y<y:
                            box.append(img[i+X,j+Y])
            ret[i,j]=min(box)
    return ret
    
def opening_closing(img):
    inter=Erosion(img)
    inter1=Dilation(inter)
    inter2=Dilation(inter1)
    ret=Erosion(inter2)
    return ret
    
def closing_opening(img):
    inter=Dilation(img)
    inter1=Erosion(inter)
    inter2=Erosion(inter1)
    ret=Dilation(inter2)
    return ret

def SNR_ratio(img,img_n):
    mu_num=0
    mu_noise_num=0
    for i in range (x):
        for j in range (y):
            mu_num+=img[i,j]
            mu_noise_num+=(img_n[i,j]-img[i,j])
    mu=mu_num/(x*y)
    mu_noise=mu_noise_num/(x*y)
    
    vs_num=0
    vn_num=0
    for i in range (x):
        for j in range (y):
            vs_num+=(img[i,j]-mu)**2
            vn_num+=(img_n[i,j]-img[i,j]-mu_noise)**2
    VS=vs_num/(x*y)
    VN=vn_num/(x*y)
    
    SNR=20*math.log10((VS/VN)**0.5)
    return SNR


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
    print(ms,mn)
    VS=0
    VN=0
    for i in range(row):
        for j in range(col):
            VS+=(c1[i][j]-ms)**2
            VN+=(n2[i][j]-c1[i][j]-mn)**2
    print(VS,VN)
    VS=VS/(row*col)
    VN=VN/(row*col)

    print(VS,VN)
    ans=20*math.log10((VS**0.5)/(VN**0.5))
    return ans

#print("Noise")
#cv2.imwrite("lena_Gau10.jpg",img_Gau10)
df=pd.DataFrame(img_Gau10)
df.to_csv("kuo_Gau10.csv")
print(SNR(img_ori,img_Gau10))
#cv2.imwrite("lena_Gau30.jpg",img_Gau30)
#print(SNR_ratio(img_ori,img_Gau30))
#cv2.imwrite("lena_Salt005.jpg",img_Salt005)
#print(SNR_ratio(img_ori,img_Salt005))
#cv2.imwrite("lena_Salt01.jpg",img_Salt01)
#print(SNR_ratio(img_ori,img_Salt01))


#print("box_filter_3x3")
img_Gau10_bf3=box_filter_3x3(img_Gau10)
print(SNR(img_ori,img_Gau10_bf3))
#cv2.imwrite("lena_Gau10_bf3.jpg",img_Gau10_bf3)
#print(SNR_ratio(img_ori,img_Gau10_bf3))
#img_Gau30_bf3=box_filter_3x3(img_Gau30)
#cv2.imwrite("lena_Gau30_bf3.jpg",img_Gau30_bf3)
#print(SNR_ratio(img_ori,img_Gau30_bf3))
#img_Salt005_bf3=box_filter_3x3(img_Salt005)
#cv2.imwrite("lena_Salt005_bf3.jpg",img_Salt005_bf3)
#print(SNR_ratio(img_ori,img_Salt005_bf3))
#img_Salt01_bf3=box_filter_3x3(img_Salt01)
#cv2.imwrite("lena_Salt01_bf3.jpg",img_Salt01_bf3)
#print(SNR_ratio(img_ori,img_Salt01_bf3))

#print("box_filter_5x5")
#img_Gau10_bf5=box_filter_5x5(img_Gau10)
#cv2.imwrite("lena_Gau10_bf5.jpg",img_Gau10_bf5)
#print(SNR_ratio(img_ori,img_Gau10_bf5))
#img_Gau30_bf5=box_filter_5x5(img_Gau30)
#cv2.imwrite("lena_Gau30_bf5.jpg",img_Gau30_bf5)
#print(SNR_ratio(img_ori,img_Gau30_bf5))
#img_Salt005_bf5=median_filter_5x5(img_Salt005)
#cv2.imwrite("lena_Salt005_bf5.jpg",img_Salt005_bf5)
#print(SNR_ratio(img_ori,img_Salt005_bf5))
#img_Salt01_bf5=median_filter_5x5(img_Salt01)
#cv2.imwrite("lena_Salt01_bf5.jpg",img_Salt01_bf5)
#print(SNR_ratio(img_ori,img_Salt01_bf5))

#print("median_filter_3x3")
#img_Gau10_mf3=median_filter_3x3(img_Gau10)
#cv2.imwrite("lena_Gau10_mf3.jpg",img_Gau10_mf3)
#print(SNR_ratio(img_ori,img_Gau10_mf3))
#img_Gau30_mf3=median_filter_3x3(img_Gau30)
#cv2.imwrite("lena_Gau30_mf3.jpg",img_Gau30_mf3)
#print(SNR_ratio(img_ori,img_Gau30_mf3))
#img_Salt005_mf3=median_filter_3x3(img_Salt005)
#cv2.imwrite("lena_Salt005_mf3.jpg",img_Salt005_mf3)
#print(SNR_ratio(img_ori,img_Salt005_mf3))
#img_Salt01_mf3=median_filter_3x3(img_Salt01)
#cv2.imwrite("lena_Salt01_mf3.jpg",img_Salt01_mf3)
#print(SNR_ratio(img_ori,img_Salt01_mf3))

#print("median_filter_5x5")
##img_Gau10_mf5=median_filter_5x5(img_Gau10)
#cv2.imwrite("lena_Gau10_mf5.jpg",img_Gau10_mf5)
#print(SNR_ratio(img_ori,img_Gau10_mf5))
#img_Gau30_mf5=median_filter_5x5(img_Gau30)
#cv2.imwrite("lena_Gau30_mf5.jpg",img_Gau30_mf5)
#print(SNR_ratio(img_ori,img_Gau30_mf5))
#img_Salt005_mf5=median_filter_5x5(img_Salt005)
#cv2.imwrite("lena_Salt005_mf5.jpg",img_Salt005_mf5)
#print(SNR_ratio(img_ori,img_Salt005_mf5))
#img_Salt01_mf5=median_filter_5x5(img_Salt01)
#cv2.imwrite("lena_Salt01_mf5.jpg",img_Salt01_mf5)
#print(SNR_ratio(img_ori,img_Salt01_mf5))

#print("Opening_Closing")
#img_Gau10_OC=opening_closing(img_Gau10)
#cv2.imwrite("lena_Gau10_oc.jpg",img_Gau10_OC)
#print(SNR_ratio(img_ori,img_Gau10_OC))
#img_Gau30_OC=opening_closing(img_Gau30)
#cv2.imwrite("lena_Gau30_oc.jpg",img_Gau30_OC)
#print(SNR_ratio(img_ori,img_Gau30_OC))
#img_Salt005_OC=opening_closing(img_Salt005)
#cv2.imwrite("lena_Salt005_oc.jpg",img_Salt005_OC)
#print(SNR_ratio(img_ori,img_Salt005_OC))
#img_Salt01_OC=opening_closing(img_Salt01)
#cv2.imwrite("lena_Salt01_oc.jpg",img_Salt01_OC)
#print(SNR_ratio(img_ori,img_Salt01_OC))

#print("Closing_Opening")
#img_Gau10_CO=closing_opening(img_Gau10)
#cv2.imwrite("lena_Gau10_co.jpg",img_Gau10_CO)
#print(SNR_ratio(img_ori,img_Gau10_CO))
#img_Gau30_CO=closing_opening(img_Gau30)
#cv2.imwrite("lena_Gau30_co.jpg",img_Gau30_CO)
#print(SNR_ratio(img_ori,img_Gau30_CO))
#img_Salt005_CO=closing_opening(img_Salt005)
#cv2.imwrite("lena_Salt005_co.jpg",img_Salt005_CO)
#print(SNR_ratio(img_ori,img_Salt005_CO))
#img_Salt01_CO=closing_opening(img_Salt01)
#cv2.imwrite("lena_Salt01_co.jpg",img_Salt01_CO)
#print(SNR_ratio(img_ori,img_Salt01_CO))

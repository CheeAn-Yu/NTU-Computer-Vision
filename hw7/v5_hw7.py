import cv2
import numpy as np
import copy

neighbor4 = [(1,0), (0,-1), (-1,0), (0,1)]
neighbor8 = [(1,0), (0,-1), (-1,0), (0,1), (1,1), (1,-1), (-1,-1), (-1,1)]

def binarize(img):
    r, c = img.shape
    b_img = np.zeros(img.shape, dtype=np.uint8)

    for i in range(r):
        for j in range(c):
            if img[i][j] >= 128:
                b_img[i][j] = 255
            else:
                b_img[i][j] = 0

    return b_img

def downsample(img):
    r, c = (int)(img.shape[0] / 8), (int)(img.shape[1] / 8)
    d_img = np.zeros([r, c], dtype=np.uint8)

    for i in range(r):
        for j in range(c):
            d_img[i][j] = img[i*8][j*8]

    return d_img

def h(b, c, d, e):
    if b != c:
        return 's'
    else:
        if (d != b or e != b):
            return 'q'
        else:
            return 'r'

def f(a1, a2, a3, a4):
    if a1 == 'r' and a2 == 'r' and a3 == 'r' and a4 == 'r':
        return 5
    else:
        n = 0
        
        if a1 == 'q':
            n += 1
        if a2 == 'q':
            n += 1
        if a3 == 'q':
            n += 1
        if a4 == 'q':
            n += 1

        return n

def yokoi(img):
    r, c = img.shape
    matrix = np.zeros(img.shape, dtype=int)

    for i in range(r):
        for j in range(c):
            if img[i][j] == 255:
                
                x = [0 for i in range(9)]
                x[0] = img[i][j]
                count = 0

                for m,n in neighbor8:
                    count += 1
                    if 0 <= i+m < 64 and 0 <= j+n < 64:
                        x[count] = img[i+m][j+n]
                
                a1 = h(x[0], x[1], x[6], x[2])
                a2 = h(x[0], x[2], x[7], x[3])
                a3 = h(x[0], x[3], x[8], x[4])
                a4 = h(x[0], x[4], x[5], x[1])
                
                matrix[i][j] = f(a1, a2, a3, a4)
                
    return matrix

def pair_relationship(matrix):
    # 1: p, 2: q
    r, c = matrix.shape
    res = np.zeros(matrix.shape, dtype=int)
    
    for i in range(r):
        for j in range(c):
            
            if matrix[i][j] != 1: # Yokoi number != 1
                res[i][j] = 2  # Set to q
            else:   #Yokoi number == 1
                flag = True

                for m, n in neighbor4:
                    if 0 <= i+m < r and 0 <= j+n < c:
                        if matrix[i+m][j+n] == 1:  # Exist a neighbor' Yokoi number = 1
                            res[i][j] = 1   # Set to p
                            flag = False
                            break

                if flag:
                    res[i][j] = 2
    
    return res

def hh(b, c, d, e):
    if b == c and (b != d or b != e):
        return 1
    else:
        return 0

def ff(a1, a2, a3, a4):
    n = 0

    if a1 == 1:
        n += 1
    if a2 == 1:
        n += 1
    if a3 == 1:
        n += 1
    if a4 == 1:
        n += 1

    return n

def shrink(img, matrix):
    r, c = img.shape
    flag = False

    for i in range(r):
        for j in range(c):
            if img[i][j] == 255:
                
                x = [0 for i in range(9)]
                x[0] = img[i][j]
                index = 0

                for m, n in neighbor8:
                    index += 1
                    if 0 <= i+m < r and 0 <= j+n < c:
                        x[index] = img[i+m][j+n]

                a1 = hh(x[0], x[1], x[6], x[2])
                a2 = hh(x[0], x[2], x[7], x[3])
                a3 = hh(x[0], x[3], x[8], x[4])
                a4 = hh(x[0], x[4], x[5], x[1])
                
                number = ff(a1, a2, a3, a4)
                
                if number == 1: # Yokoi number = 1 (edge)
                    if matrix[i][j] == 1:
                        img[i][j] = 0
                        flag = True
    
    return img, flag


if __name__=='__main__':

    image = cv2.imread('Lena.jpg', cv2.IMREAD_GRAYSCALE)

    downsample_image = downsample(binarize(image))
    thinning_image = copy.deepcopy(downsample_image)

    check = True
    
    while check:

        yokoi_matrix = yokoi(thinning_image)

        paired_matrix = pair_relationship(yokoi_matrix)
        
        thinning_image, check = shrink(thinning_image, paired_matrix)
        
    cv2.imshow("image", thinning_image)
    cv2.imwrite("thinned image.jpg", thinning_image)
    cv2.waitKey(0)

    

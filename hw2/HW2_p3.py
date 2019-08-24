'''
HW2_P3 - Connected component

class Table() use to set label_table and runlength_table
def set_dictval use to change the value of tuple in dict

1. make image be a binary image by thresholding with 128
2. label all pixels
3. do Top-down pass
4. do Bottom-up pass
5. check that weather each label has more than 500 pixels
6. set these label as boundboxes with left, top, right, down
   (boundboxes[label] = (left, top, right, down))
7. draw bounding boxes by cv2.rectangle (change Gray to RGB)
'''

import cv2
import numpy as np
import pandas as pd
def findmin(label, row1, col1, row2, col2):
    if label[row2][col2] != 0:
        answer = min(label[row1][col1], label[row2][col2])
    else:
        answer = label[row1][col1]

    return answer

def set_dictval(dic, val, itr):
    dic = list(dic)
    dic[itr] = val
    return tuple(dic)

if __name__ == '__main__':
    img = cv2.imread("lena512.bmp",0)
    
    height, width = img.shape
    
    label = np.zeros((height, width),dtype=np.int)
    un_label = 1
    
    #change image to binary_image
    for i in range(height):
        for j in range(width):
            if img[i][j] >= 128:
                img[i][j] = 255
            else:
                img[i][j] = 0
    
    #init label
    for i in range(height):
        for j in range(width):
            if img[i][j] == 255:
                label[i][j] = un_label
                un_label += 1
    df=pd.DataFrame(label)
    df.to_csv("TrueLabel.csv")
    change = True
    while change:
        change = False
        #top-down pass
        for i in range(height):
            for j in range(width):
                if label[i][j] != 0:
                    temp = 0
                    if i != 0 and j != 0:
                        temp = findmin(label, i, j, i-1, j)
                        temp2 = min(temp,label[i][j-1])
                        if temp2 != 0:
                            temp = temp2
                    elif i != 0 and j == 0:
                        temp = findmin(label, i, j, i-1, j)
                    elif i == 0 and j != 0:
                        temp = findmin(label, i, j, i, j-1)
                    #else:
                    #    temp = label[i][j]

                    if temp != label[i][j]:
                        change = True
     
                    label[i][j] = temp

        #bottom-up pass
        for i in range(height-1, -1, -1):
            for j in range(width-1, -1, -1):
                if label[i][j] != 0:
                    temp = 0
                    if i != height-1 and j != width-1:
                        temp = findmin(label, i, j, i+1, j)
                        temp2 = min(temp,label[i][j+1])
                        if temp2 != 0:
                            temp = temp2
                    elif i != height-1 and j == width-1:
                        temp = findmin(label, i, j, i+1, j)
                    elif i == height-1 and j != width-1:
                        temp = findmin(label, i, j, i, j+1)
                    #else:
                    #   temp = label[i][j]

                    if temp != label[i][j]:
                        change = True

                    label[i][j] = temp

    #count component pixels        
    count_pixels = {}
    for i in range(height):
        for j in range(width):
            if label[i][j] != 0:
                if not label[i][j] in count_pixels.keys():
                    count_pixels[label[i][j]] = 0
                else:
                    count_pixels[label[i][j]] += 1
    
    #set bounding boxes 
    boundboxes = {}
    for i in range(height):
        for j in range(width):
            temp_label = label[i][j]
            if temp_label in count_pixels.keys() and count_pixels[temp_label] >= 500:
                if not temp_label in boundboxes.keys():
                    boundboxes[temp_label] = (j, i, j, i)
                else:
                    if boundboxes[temp_label][0] > j:
                        boundboxes[temp_label] = set_dictval(boundboxes[temp_label], j, 0)
                    elif boundboxes[temp_label][1] > i:
                        boundboxes[temp_label] = set_dictval(boundboxes[temp_label], i, 1)
                    elif boundboxes[temp_label][2] < j:
                        boundboxes[temp_label] = set_dictval(boundboxes[temp_label], j, 2)
                    elif boundboxes[temp_label][3] < i:
                        boundboxes[temp_label] = set_dictval(boundboxes[temp_label], i, 3)

    #draw bounding boxes and cross
    rgb_img = cv2.cvtColor(img, cv2.COLOR_GRAY2RGB)
    for i in boundboxes.keys():
        cv2.rectangle(rgb_img, (boundboxes[i][0], boundboxes[i][1]),(boundboxes[i][2], boundboxes[i][3]),(0,0,255))
        
        center_x = (int)((boundboxes[i][0] + boundboxes[i][2])/2)
        center_y = (int)((boundboxes[i][1] + boundboxes[i][3])/2)
        cv2.line(rgb_img, (center_x-5, center_y),(center_x+5, center_y),(0,0,255))
        cv2.line(rgb_img, (center_x, center_y-5),(center_x, center_y+5),(0,0,255))

    cv2.imwrite("lena_connected_component.bmp",rgb_img)
    cv2.imshow("Img",rgb_img)
    cv2.waitKey(0)


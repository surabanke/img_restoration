#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jan  9 11:27:37 2022

@author: eunhwalee
"""

# merge img 2x2

import numpy as np
import cv2
import os



global can

def compare(r,a,max_ed,max_index):
    cnt_lst_a = []
    cnt_lst = []
    for i in range(len(r)):
        
        for j in range(len(a)):
            cnt = 0
            #cnt_a = 0
            r_mat = r[i]
            a_mat = a[j]
            for k in range(len(r_mat)):
                #diff = abs(r_mat[k] - a_mat[k])
                if r_mat[k] == a_mat[k] and (r_mat[k] != 0):
                    cnt += 1

            cnt_lst_a.append(cnt)
            cnt_lst.append([i,j])

    print(cnt_lst_a)        
    if max(cnt_lst_a) > max_ed :
        index = cnt_lst_a.index(max(cnt_lst_a))
        i = cnt_lst[index][0]
        j = cnt_lst[index][1]
        
        if (i != j):
            max_ed = max(cnt_lst_a)
            max_index[0] = i
            max_index[1] = j
            #print(max_ed,max_index)

                

    return max_index, max_ed

def sobel(img):
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    dx = cv2.Sobel(img, cv2.CV_32F, 1, 0, 3) 
    dy = cv2.Sobel(img, cv2.CV_32F, 0, 1, 3)


    mag = cv2.magnitude(dx, dy) 
    mag = np.round(mag,1)
    mag = np.clip(mag, 0, 255).astype(np.uint8) 

    
    #dst = np.zeros(img.shape[:2], np.uint8) 
    #mag[mag > 170] = 255
    #mag[mag < 20] = 0
    
    return mag

              
def rotation(img):
    img = cv2.rotate(img,cv2.ROTATE_90_COUNTERCLOCKWISE) 
    return img


def matching_and_merge(add_img,root):
    
    global can
    can = 0
    
    if root.shape[0] > root.shape[1]:
        root = rotation(root)
        
    if root.shape[0] != add_img.shape[0]:
        add_img = rotation(add_img)
        
    width = root.shape[1]
    height = root.shape[0]
    
    max_edv =0
    max_edbv = 0
    max_indexv = [0,0]
    
    max_edh =0
    max_edbh = 0
    max_indexh = [0,0]
    
    if root.shape[0] != root.shape[1]:

        add_f = cv2.flip(add_img,0)
        add_m = cv2.flip(add_img,1)  
        add_mf = cv2.flip(add_m,0)
        
        add_lst = [add_img,add_f,add_m,add_mf]
    else:
    
        add_f = cv2.flip(add_img,0)
        add_m = cv2.flip(add_img,1)  
        add_mf = cv2.flip(add_m,0)
    
        add_fr  = rotation(add_f) 
        add_mr  = rotation(add_m)
        add_mfr  = rotation(add_mf)
        add_imgr = rotation(add_img)

        add_lst = [add_img,add_f,add_m,add_mf,add_imgr,add_fr,add_mr,add_mfr]
            
        
    for j in range(len(add_lst)):
            
        gray = sobel(root)

        gray_1 = sobel(add_lst[j])
            
        bin0 = gray[0]
        bin1 = gray[:,0]
        bin2 = gray[height -1]
        bin3 = gray[:,width -1]
            
        bin_rv = [bin0,bin2]
        bin_rh = [bin1,bin3]

            
        bin01 = gray_1[0]
        bin11 = gray_1[:,0]
        bin21 = gray_1[height -1]
        bin31 = gray_1[:,width -1]
            
        bin_av = [bin01,bin21]
        bin_ah = [bin11,bin31]

        max_indexv,max_edv = compare(bin_rv,bin_av,max_edbv,max_indexv) # vconcat
        max_indexh,max_edh = compare(bin_rh,bin_ah,max_edbh,max_indexh) # hconcat
        # print(max_indexv, max_edv)
        # print(max_indexh, max_edh)
            
        if max_edv > max_edbv :
            max_edbv = max_edv
            
            index_add_v = j
                
        if max_edh > max_edbh:
            max_edbh = max_edh
          
            index_add_h = j
                
            
    if max_edv > max_edh:
        if max_indexv[0] == 0 and max_indexv[1] == 1:
            can = cv2.vconcat([add_lst[index_add_v],root])
                
        elif max_indexv[0] == 1 and max_indexv[1] == 0:
            can = cv2.vconcat([root,add_lst[index_add_v]])
    else:
        if max_indexh[0] ==0 and max_indexh[1] == 1:
            can = cv2.hconcat([add_lst[index_add_h],root])
                
        elif max_indexh[0] == 1 and max_indexh[1] == 0:
            can = cv2.hconcat([root,add_lst[index_add_h]])
                

        
    return can
            

fin_lst = []
path =  "/Users/eunhwalee/Desktop/divide_image/"
files = os.listdir(path)
#files.remove(files[1])

root = cv2.imread(path+files[0])

files.remove(files[0])


for i in range(len(files)):
    add_img = cv2.imread(path + files[i])
    #add_img = cv2.Canny(add_img,50,200)
    cann = matching_and_merge(add_img,root)
    if (type(cann) is np.ndarray) == True:
        fin_lst.append(cann)
        files.remove(files[i])
        break

    
img = cv2.cvtColor(root, cv2.COLOR_BGR2HSV)

root = cv2.imread(path +files[0])

add_img = cv2.imread(path + files[1])

cann_1 = matching_and_merge(add_img,root)
fin_lst.append(cann_1)

root = fin_lst[0]
add_img = fin_lst[1]
      
width = root.shape[1]
height = root.shape[0]


final_img = matching_and_merge(add_img,root)



cv2.imwrite(path + 'final_img.png',final_img)





        
        
        
        
        
        
        
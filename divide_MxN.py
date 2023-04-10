#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jan  7 18:14:59 2022

@author: eunhwalee
"""

# divide img MxN

from PIL import Image
import numpy as np
import os
import cv2
import sys

path = "/Users/eunhwalee/Desktop/"
img = Image.open(path + 'sibadog.png')
extend = img.width

numpy_image=np.array(img)  

test = "test"
prob = 0.5



def make_size(img_len,div):
    cnt = 0
    for i in range(img_len):
        
        if img_len%div == 0:
            return cnt
            break
        
        else:
            img_len += 1
            cnt += 1


def divide_img(img,column,row,test):
    
    width = np.size(img)[0]
    height = np.size(img)[1]
    
    
    if width%column  != 0:
        
        cnt = make_size(width,column)
        width = width + cnt
        
    if height%row != 0:
        
        cnt = make_size(height,row)
        height = height + cnt
        
        
    img = img.resize((width,height), Image.LANCZOS)
    os.makedirs(path + 'divide_image', exist_ok=True)
    img.save(path + 'img.png')
    w = int(width/column)
    h = int(height/row)
    
    
    
    for i in range(0,width,w):
        for j in range(0,height,h):
            box = (i, j, i+w, j+h)
            a = img.crop(box)
            numpy_a=np.array(a) 
            a = cv2.cvtColor(numpy_a, cv2.COLOR_BGR2RGB)


            
            mirror = np.random.rand()
            flip = np.random.rand()
            rotate = np.random.rand()
            
            if rotate > prob:
                h_a, w_a, channel = a.shape
                a = cv2.rotate(a, cv2.ROTATE_90_CLOCKWISE)
            
            
            if mirror > prob:
                a = cv2.flip(a,1)

            if flip > prob:
                a = cv2.flip(a,0)



               
                
                    
            rand_name = mirror + flip + rotate
            
            #os.makedirs(path + 'divide_image', exist_ok=True)
            
            cv2.imwrite(path + 'divide_image/'+ test +str(rand_name)+'.png',a)
            
        
        

    

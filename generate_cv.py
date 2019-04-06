# -*- coding: utf-8 -*-
"""
Created on Sat Apr  6 12:46:05 2019

@author: FOLEFAC
"""
import cv2
import numpy as np
import argparse
import os




parser = argparse.ArgumentParser()
parser.add_argument('--source_pics_dir', type=str, default='source_pics')
FLAGS = parser.parse_args()


def get_images():
    '''
    find image files in test data path
    :return: list of files found
    '''
    files = []
    exts = ['jpg', 'png', 'jpeg', 'JPG','PNG']
    for parent, dirnames, filenames in os.walk(FLAGS.source_pics_dir):
        for filename in filenames:
            for ext in exts:
                if filename.endswith(ext):
                    files.append(os.path.join(parent, filename))
                    break
    print('Found {} images'.format(len(files)))
    return files






def join_images(background,foreground):
    '''
    joins two images, one on top of the other.
    inputs:
    background: the background image
    foreground: the foreground image
    
    :return: the joint image
    '''
    
    img1 = cv2.imread(background)
    img2 = cv2.imread(foreground)
    
    img1=cv2.resize(img1,(320,320))
    img2=cv2.resize(img2,(320,320))
    
    
    rows=320
    cols=320
    channels=3
    roi = img1[0:rows, 0:cols ]
    
    img2gray = cv2.cvtColor(img2,cv2.COLOR_BGR2GRAY)
    ret, mask = cv2.threshold(img2gray, 10, 255, cv2.THRESH_BINARY)
    mask_inv = cv2.bitwise_not(mask)
    
    img1_bg = cv2.bitwise_and(roi,roi,mask = mask_inv)
    
    img2_fg = cv2.bitwise_and(img2,img2,mask = mask)
    
    
    dst = cv2.add(img1_bg,img2_fg)
    img1[0:rows, 0:cols ] = dst
    
    background1=os.path.splitext(background)[0]
    background2=os.path.splitext(background)[1]
    background=background1+'new'+background2
    print(background)
    
    cv2.imwrite(background,img1)

def main(argv=None):
    
    img_list = get_images()
    
    for img_file in img_list:
               
        join_images(img_file,'f.jpg')
    
    


    
    
if __name__ == '__main__':
    main()

    

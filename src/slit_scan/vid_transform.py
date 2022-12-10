import os 
import cv2 as cv
import numpy as np 
#import sys 
from time import sleep
import pygame as pg
#jit numba

current_path = os.getcwd()
print(f'Current path is: {current_path}')

#progressbar
def progress(percent=0, width=30):
    left = width * percent // 100
    right = width - left
    print('\r[', '#' * left, ' ' * right, ']',
          f' {percent:.0f}%',
          sep='', end='', flush=True)

#video params
vid     = cv.VideoCapture('video/earth.mp4')
width   = int(vid.get(cv.CAP_PROP_FRAME_WIDTH))
height  = int(vid.get(cv.CAP_PROP_FRAME_HEIGHT))
fps     = vid.get(cv.CAP_PROP_FPS)
nframes = int(vid.get(cv.CAP_PROP_FRAME_COUNT))
len     = round(nframes/fps,2) #// 1000
print(f'video {len} sec {nframes} frames {width}x{height} @{fps} fps')
slit_size = int(width//nframes + 1)
print(f'slit size = {slit_size}')

#draw a line
start_point = (int(width//2),0)
end_point = (int(width/2),height)
color = (255,0,0)
thickness = slit_size*3
print(f'line: start {start_point} end {end_point}')

#output template
row_size = height, 1, 3
out_img = (np.zeros(row_size, dtype=np.uint8))

#
vid.set(cv.CAP_PROP_POS_FRAMES,0)
for i in range(nframes):
    cv.imshow('window', out_img)
    cv.waitKey(1)
    ret, frame = vid.read()
    #left to right
    #out_img = cv.hconcat([out_img,frame[0:int(height), i:slit_size*(i+1)].copy()])
    #left static
    #out_img = cv.hconcat([out_img,frame[0:int(height), 0:slit_size].copy()])
    #center static
    out_img = cv.hconcat([out_img,frame[0:int(height), int(width//2):int(width//2+slit_size)].copy()])
    progress(round(i*slit_size/nframes*100))
    frame = cv.line(frame,start_point,end_point,color,thickness)
    cv.imshow('frame', frame)

cv.imshow('window', out_img)

cv.waitKey(0)
vid.release()
cv.destroyAllWindows()
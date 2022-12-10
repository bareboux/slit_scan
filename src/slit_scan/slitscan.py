#import os 
import cv2 as cv
#import numpy as np 
#import sys 
#from time import sleep
#import pygame as pg
#jit numba

#добавить источник вебкамера
#добавить скорость смещения среза
#смещение на основе итератора а не номера кадра, ограничение на выход за границы кадра
#нормально оформить модуль, принимать аргументы снаружи
#приклеивать изображение к видео по линии среза
#диагональные срезы
#переписать на numpy
class SlitScanner:
    def __init__(self, path = 'video/earth.mp4', direction = 'horizontal', slit_size = 1, start_position = 50, finish_position = None, show_ui = False):
        self.path = path
        self.show_ui = show_ui
        self.dir  = direction
        self.vid  = cv.VideoCapture(self.path)
        self.width, self.height = int(self.vid.get(cv.CAP_PROP_FRAME_WIDTH)), int(self.vid.get(cv.CAP_PROP_FRAME_HEIGHT))
        self.nframes = int(self.vid.get(cv.CAP_PROP_FRAME_COUNT))
        self.fps = self.vid.get(cv.CAP_PROP_FPS)
        len = round(self.nframes/self.fps,2) 
        print(f'video {len} sec {self.nframes} frames {self.width}x{self.height} @{self.fps} fps')
        
        self.start_pos = start_position
        self.slit_size = slit_size
        if finish_position is None:
            self.finish_pos = start_position
            self.shift = False
        elif finish_position != start_position:
            self.shift = True
            self.finish_pos = finish_position
            if finish_position < start_position:
                self.slit_size = -1*slit_size
        else:
            self.shift = False
            self.finish_pos = finish_position

        if self.dir == 'horizontal':
            self.start_pos = int(self.width * self.start_pos/100)
            self.finish_pos = int(self.width * self.finish_pos/100)
        elif self.dir == 'vertical':
            self.start_pos = int(self.height * self.start_pos/100)
            self.finish_pos = int(self.height * self.finish_pos/100)

    #load next frame
    def get_frame(self):
        self.ret, self.frame = self.vid.read()
        self.frame_num = self.vid.get(cv.CAP_PROP_POS_FRAMES)
        #if not self.ret:
            #exit()
        return self.frame

    #source video & result output
    def draw(self):
        scale_factor = 500/self.width
        resized_frame = cv.resize(self.frame, None, fx = scale_factor, fy = scale_factor, interpolation= cv.INTER_AREA)
        cv.imshow('frame', resized_frame)
        cv.imshow('out_img', self.out_img)
        if cv.waitKey(1) & 0xFF == ord('q'):
            self.vid.release()
            cv.destroyAllWindows()

    #init empty output
        #row_size = self.height, 1, 3

    def get_slice_range(self):
        #frame_num заменить на итератор
        if self.slit_size > 0:
            if self.dir == 'horizontal':
                x_start = self.start_pos + (self.frame_num - 1)*self.slit_size*self.shift
                y_start = 0
                x_end   = x_start + self.slit_size
                y_end   = self.height
            elif self.dir == 'vertical':
                x_start = 0
                y_start = self.start_pos + (self.frame_num - 1)*self.slit_size*self.shift
                x_end   = self.width
                y_end   = y_start + self.slit_size
        elif self.slit_size < 0:
            if self.dir == 'horizontal':
                x_end   = self.start_pos + (self.frame_num - 1)*self.slit_size*self.shift
                y_start = 0
                x_start   = x_end + self.slit_size
                y_end   = self.height
            elif self.dir == 'vertical':
                x_start = 0
                y_end   = self.start_pos + (self.frame_num - 1)*self.slit_size*self.shift
                x_end   = self.width
                y_start = y_end + self.slit_size
        #print(f'x_start = {x_start}, y_start = {y_start}, x_end = {x_end}, y_end = {y_end}')
        #return x_start, y_start, x_end, y_end
        return dict(x_start = int(x_start), y_start = int(y_start), x_end = int(x_end), y_end = int(y_end))

    def slice_image(self, pos):
        temp_slice = self.frame[pos.get('y_start'):pos.get('y_end'), pos.get('x_start'):pos.get('x_end')].copy()
        if self.frame_num == 1:
            if self.dir == 'horizontal':
                self.out_img = temp_slice
            elif self.dir == 'vertical':
                self.out_img = temp_slice
        else:
            if self.slit_size > 0:
                if self.dir == 'horizontal':
                    self.out_img = cv.hconcat([self.out_img, temp_slice])
                elif self.dir == 'vertical':
                    self.out_img = cv.vconcat([self.out_img, temp_slice])
            elif self.slit_size < 0:
                if self.dir == 'horizontal':
                    self.out_img = cv.hconcat([temp_slice, self.out_img])
                elif self.dir == 'vertical':
                    self.out_img = cv.vconcat([temp_slice, self.out_img])
        self.frame = cv.rectangle(self.frame, (pos.get('x_start'),pos.get('y_start')), (pos.get('x_end'),pos.get('y_end')), color = (255,0,0), thickness = self.slit_size)
    
    def save_image(self):
        cv.imwrite('out/result.jpg', self.out_img)
        print('\nimage saved!')

    @staticmethod
    def progress(percent=0, width=30):
        left = width * percent // 100
        right = width - left
        print('\r[', '#' * left, ' ' * right, ']',
            f' {percent:.0f}%',
            sep='', end='', flush=True)

    def run(self):
        self.get_frame()
        while self.ret:
            self.slice_image(self.get_slice_range())
            if self.show_ui: self.draw()
            self.get_frame()
            self.progress(int(self.frame_num/self.nframes*100))
        if cv.waitKey(0) & 0xFF == ord('s'):
            self.save_image()
        self.vid.release()
        cv.destroyAllWindows()
            
if __name__ == '__main__':
    app = SlitScanner()
    app.run()
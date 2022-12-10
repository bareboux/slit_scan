import cv2 as cv
import numpy as np

# define a video capture object
vid = cv.VideoCapture(0)
width   = int(vid.get(cv.CAP_PROP_FRAME_WIDTH))
height  = int(vid.get(cv.CAP_PROP_FRAME_HEIGHT))
fps     = vid.get(cv.CAP_PROP_FPS)
nframes = int(vid.get(cv.CAP_PROP_FRAME_COUNT))
len     = round(nframes/fps,2) #// 1000
print(f'video {len} sec {nframes} frames {width}x{height} @{fps} fps')
#slit_size = int(width//nframes + 1)
slit_size = 1

row_size = height, 1, 3
out_img = (np.zeros(row_size, dtype=np.uint8))

while(True):
      
    # Capture the video frame
    # by frame
    ret, frame = vid.read()
  
    # Display the resulting frame
    cv.imshow('frame', frame)
    cv.imshow('window', out_img)
    out_img = cv.hconcat([out_img,frame[0:int(height), int(width//2):int(width//2+slit_size)].copy()])
      
    # the 'q' button is set as the
    # quitting button you may use any
    # desired button of your choice
    if cv.waitKey(1) & 0xFF == ord('q'):
        break
  
# After the loop release the cap object
vid.release()
# Destroy all the windows
cv.destroyAllWindows()


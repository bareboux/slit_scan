from slitscan import SlitScanner as sc
import time
start_time = time.time()
obj = sc(path = 'video/crowd.mp4', direction = 'vertical', slit_size = 1, start_position = 40, finish_position=40, show_ui = True)
obj.run()
print("--- %s seconds ---" % (time.time() - start_time))

# A diagonal slice through images to make a HD frame
""" outw,outh=w,min(h,frameno)
posarr=numpy.zeros((outh,outw,3),numpy.uint8)
negarr=numpy.zeros((outh,outw,3),numpy.uint8)
print("Creating output images for diagonal horizontal slices...")
for frm in xrange(0,frameno-outh+1):
    for H in xrange(0,outh):
        posarr[H,:,:]=mastarr[frm+H,H,:,:]
        negarr[H,:,:]=mastarr[frm+outh-1-H,H,:,:]
    posimage=Image.fromarray(posarr)
    posimage.save(os.path.join(outdir,"DiagonalPos%05d.png"%frm))
    negimage=Image.fromarray(negarr)
    negimage.save(os.path.join(outdir,"DiagonalNeg%05d.png"%frm)) """
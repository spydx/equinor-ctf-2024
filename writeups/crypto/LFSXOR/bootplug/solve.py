import sys

import numpy
import matplotlib.pyplot as plt
from PIL import Image

def decrypt(in_img, out_img):
    in_img = plt.imread(in_img)[:, :, 0]
    height = len(in_img)
    width = len(in_img[0])
    
    imarr = numpy.zeros((height, width, 3), dtype='uint8')
    crib = [in_img[(i//2048),i%2048] for i in range(9362)] # grab the first 9362 pixels
    
    for y in range(height):
        for x in range(width):
            imarr[y,x] = int(in_img[y,x] ^ crib[(y*2048 + x)%len(crib)])
    
    im = Image.fromarray(imarr.astype('uint8')).convert('RGB')
    im.save(out_img)

if __name__=='__main__':
    IN_IMG = sys.argv[1]
    OUT_IMG = sys.argv[2]
    decrypt(IN_IMG, OUT_IMG)
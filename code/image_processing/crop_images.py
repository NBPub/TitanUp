from pathlib import Path
from PIL import Image
import numpy as np

# folder with images
p = Path(r'')
# subfolder with inverted images
new_p = Path(p, f'{p.name} cropped')
new_p.mkdir(exist_ok = True)

# define how tightly to find boundary by pixels
jump = 50

# boundary finding functions
def y_boundary(ycheck,xcheck,color):
    for y in ycheck:
        for x in xcheck:
            pixel = im.getpixel((x,y))
            if pixel != color:
                return y
def x_boundary(ycheck,xcheck,color):
    for x in xcheck:
        for y in ycheck:
            pixel = im.getpixel((x,y))
            if pixel != color:
                return x

# iterate through folder
for child in p.iterdir():
    if child.suffix == '.png':
        im = Image.open(child)
        # Get upper-left corner pixel for gray color
        grey = im.getpixel((0,0))
        # image bounds
        box = im.getbbox()
        xcheck = np.arange(0,box[2],jump)
        ycheck = np.arange(0,box[3],jump)
        
        # find bounds
        top = y_boundary(ycheck,xcheck,grey)
        top -= jump
        bottom = y_boundary(ycheck[::-1],xcheck,grey)
        bottom += jump
        ycheck = np.arange(top,bottom,jump)        
        left = x_boundary(ycheck,xcheck,grey)
        left -= jump
        right = x_boundary(ycheck,xcheck[::-1],grey)
        right += jump
        
        # crop and save as new image
        new = im.crop((left, top, right, bottom))
        new.save(Path(new_p, child.name))
        print('completed',child.name)
print('\tAll Done!')



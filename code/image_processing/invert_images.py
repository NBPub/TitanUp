from pathlib import Path
from PIL import Image
import numpy as np

# folder with images
p = Path(r'')
# subfolder with inverted images
new_p = Path(p, f'{p.name} inverted')
new_p.mkdir(exist_ok = True)

for child in p.iterdir():
    if child.suffix == '.png':
        im = Image.open(child)
        
        pixels = np.array(list(im.getdata()))
        colors = np.abs(pixels - 
                 np.concatenate((255*np.ones((pixels.shape[0],3), dtype='int'), 
                 np.zeros((pixels.shape[0],1), dtype='int')), axis=1))
        
        im.putdata(list(map(tuple,colors)))
        im.save(Path(new_p, child.name))
        print('completed',child.name)
print('\tAll Done!')

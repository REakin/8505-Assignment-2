import os
import numpy as np
from PIL import Image

#load image
def load_image(path):
    img = Image.open(path)
    img = img.convert('RGB')
    img = np.array(img)
    return img

#load hidden image
def load_hidden_image(path):
    with open(path, 'rb') as f:
        img = f.read()
        return img

#save image
def save_image(path, img):
    img = Image.fromarray(img)
    img.save(path)
    return

import os, random, math
import numpy as np
import scipy.spatial.distance as dist
from PIL import Image

SUB_DIM = 100
IMG_ROOT = '/Users/conorkerrigan/Documents/GitHub/Auto-Collage/images/img_align_celeba'

def compare_colour(target_colour, source_colour):
    return dist.euclidean(source_colour, target_colour)

def average_colour(image, width, height, x=0, y=0):
        count = 0
        print(image.size)
        image = image.load()
        r, g, b = 0, 0, 0
        for s in range(x, x+width):
            for t in range(y, y+height):
                pixlr, pixlg, pixlb = image[s, t]
                r += pixlr
                g += pixlg
                b += pixlb
                count += 1
        avg = ((r/count), (g/count), (b/count))
        return avg

def find_colour_match(photo_list, colour):
    best = -1
    for photo in photo_list:
        dif = compare_colour(photo.avgColour, colour)
        if best == -1 or dif < best:
            best = dif
            match = photo
    return match

def get_concat_h(im1, im2):
    dst = Image.new('RGB', (im1.width + im2.width, im1.height))
    dst.paste(im1, (0, 0))
    dst.paste(im2, (im1.width, 0))
    return dst

def get_concat_v(im1, im2):
    dst = Image.new('RGB', (im1.width, im1.height + im2.height))
    dst.paste(im1, (0, 0))
    dst.paste(im2, (0, im1.height))
    return dst

class Photo:
    def __init__(self, path, target=False):
        self.path = IMG_ROOT+'/'+path
        self.target = target
        self.image = Image.open(self.path).resize((89,109),Image.ANTIALIAS)
        self.width, self.height = self.image.size
        print(self.path)
        self.avgColour = average_colour(self.image, self.width, self.height)

    def colour_array(self, sample_size=1):
        colour_map = []
        if self.target:
            for x in range(0, self.width):
                for y in range(0, self.height):
                    cell_colour = self.image[x, y]
                    colour_map.append(cell_colour)
        return colour_map



image_paths = os.listdir(IMG_ROOT)
image_paths = random.sample(image_paths, 500)
images = []
first = True
counter = 0

for path in image_paths:
    if first:
        target = Photo(path, first)
        target_img = Image.open(IMG_ROOT+'/'+path).resize((89,109),Image.ANTIALIAS).load()
        target.image.save("target.jpeg","JPEG")
    else:
        counter += 1
        p = (counter/len(image_paths))*100
        print(p)
        images.append(Photo(path, first))
    first = False

matches = np.empty((89,109), dtype=object)

for x in range(0,target.width):
    for y in range(0, target.height):
        colour = target_img[x,y]
        matches[x,y] = find_colour_match(images,colour)

counter = 0

img_row = None
for x in range(0,target.width):
    img_column = None
    print(100*(counter/target.width))
    for y in range(0, target.height):
        match = matches[x,y]
        if img_column != None:
            img_column = get_concat_v(img_column,match.image)
        else:
            img_column = match.image
    if img_row != None:
        img_row = get_concat_h(img_row,img_column)
    else:
        img_row = img_column
    counter += 1
print(len(matches))
img_row.save("collage.jpeg", "JPEG",optimize=True,quality=95)
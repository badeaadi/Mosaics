"""
    PROIECT MOZAIC
    
    Badea Adrian Catalin, grupa 334, anul III, FMI
"""

import os
import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt
import pdb
import glob

from add_pieces_mosaic import *
from parameters import *


def load_pieces(params: Parameters):
    
    # citeste toate cele N piese folosite la mozaic din directorul corespunzator
    # toate cele N imagini au aceeasi dimensiune H x W x C, unde:
    # H = inaltime, W = latime, C = nr canale (C=1  gri, C=3 color)
    # functia intoarce pieseMozaic = matrice N x H x W x C in params
    # pieseMoziac[i, :, :, :] reprezinta piesa numarul i
    images = [cv.imread(file) for file in glob.glob(params.small_images_dir + "*" + params.image_type)]
    
    
    if params.grayscale:
        images = [cv.cvtColor(image, cv.COLOR_BGR2GRAY) for image in images]
        images = [np.stack((image, image, image), axis = -1) for image in images]
        
    print(len(images))
    images = np.asarray(np.asarray(images)[:,:,:, :3])
    
    
    params.small_images = images
    params.small_images_np = np.asarray(images)
    
    print(params.small_images_np.shape)


    # citeste imaginile din director


    if params.show_small_images:
        for i in range(10):
            for j in range(10):
                plt.subplot(10, 10, i * 10 + j + 1)
                # OpenCV reads images in BGR format, matplotlib reads images in RGB format
                im = images[i * 10 + j].copy()
                # BGR to RGB, swap the channels
                im = im[:, :, [2, 1, 0]]
                plt.imshow(im)
        plt.show()



def compute_dimensions(params: Parameters):
    
    # calculeaza dimensiunile mozaicului
    # obtine si imaginea de referinta redimensionata avand aceleasi dimensiuni

    height, width = params.small_images_np.shape[1:3];
    
    # print(height, width);
    # 28 40 pentru colectia cu flori
    
    height_image, width_image = np.asarray(params.image).shape[:2]
    
    # print(height_image, width_image)
    # 183 275 pentru imaginea ferrari
    
    ratio_image = width_image / height_image
    params.num_pieces_vertical = int(params.num_pieces_horizontal * width / height / ratio_image)

    
    # print(params.num_pieces_vertical)
    # 95 pentru ferrari
    
    # redimensioneaza imaginea
    new_height = params.num_pieces_vertical * height
    new_width = params.num_pieces_horizontal * width
    
    print(new_height, new_width)
    # 2660 4000
    
    params.image_resized = cv.resize(params.image, (new_width, new_height))
    
    params.small_images = np.asarray(params.small_images)
    params.image_resized = np.asarray(params.image_resized)
    
    # auximage = cv.cvtColor(params.image_resized, cv.COLOR_RGB2BGR)
    # cv.imwrite('masina.png', auximage)


def build_mosaic(params: Parameters):
    # incarcam imaginile din care vom forma mozaicul
    load_pieces(params)
    # calculeaza dimensiunea mozaicului
    compute_dimensions(params)


    img_mosaic = None
    
    if params.layout == 'caroiaj':
        if params.hexagon is True:
            img_mosaic = add_pieces_hexagon(params)
        else:
            img_mosaic = add_pieces_grid(params)
            
    elif params.layout == 'aleator':
        img_mosaic = add_pieces_random(params)
    else:
        print('Wrong option!')
        exit(-1)

    return img_mosaic


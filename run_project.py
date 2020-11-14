"""
    PROIECT MOZAIC
    
    Badea Adrian Catalin, grupa 334, anul III, FMI
"""

# Parametrii algoritmului sunt definiti in clasa Parameters.



# Colectii tematice

from parameters import *
from build_mosaic import *

my_photo_names = ['bear.jpg', 'tank.jpg', 'elephant.jpg', 
                  'skyscraper.jpg', 'sunflower.jpg', 'forest.jpg']

my_collections = ['bear', 'tank', 'elephant', 
                  'skyscraper', 'sunflower', 'forest']

my_description = ['bear', 'tank', 'elephant', 
                  'skyscraper', 'sunflower', 'forest']


for name, coll,  desc in zip(my_photo_names, my_collections, my_description):
    
    params = Parameters('./../data/imaginiTematice/' + name)
    params.small_images_dir = './../data/colectiiTematice/' + coll + '/'
    img_mosaic = build_mosaic(params)
    cv.imwrite('mozaic_' + desc + '_diferite.jpg', img_mosaic)



# Colectii test

photo_names = ['ferrari.jpeg', 'romania.jpeg', 'tomJerry.jpeg', 
               'liberty.jpg', 'adams.jpg', 'obama.jpeg',]


description = ['ferrari_hexagon', 'romania_hexagon', 'tomJerry_hexagon', 
               'liberty_hexagon', 'adams_hexagon_grayscale', 'obama_hexagon_grayscale',]


for name, desc in zip(photo_names, description):
    
    params = Parameters('./../data/imaginiTest/' + name)
    
    if name in ['adams.jpg', 'obama.jpeg']:
        params.grayscale = True
    
    params.small_images_dir = './../data/colectie/' 
    img_mosaic = build_mosaic(params)
    cv.imwrite('mozaic_' + desc + '_diferite.jpg', img_mosaic)


# Creare un singur mozaic
        
name = 'alex.jpg'
desc = 'alex_haexagoane'

params = Parameters('./../data/imaginiTest/' + name)
    
params.small_images_dir = './../data/colectie/' 
img_mosaic = build_mosaic(params)
cv.imwrite('mozaic_' + desc + '_diferite.jpg', img_mosaic)


"""
    PROIECT MOZAIC
    
    Badea Adrian Catalin, grupa 334, anul III, FMI
"""

import cv2 as cv
import numpy as np
import math


# In aceasta clasa vom stoca detalii legate de algoritm si de imaginea pe care este aplicat.
class Parameters:

    def __init__(self, img_path):
        
        # numele imaginii care va fi transformata in mozaic
        
        self.image_path = img_path
        
        self.image = cv.imread(self.image_path)
        
        #self.image = cv.cvtColor(cv.imread(image_path), cv.COLOR_BGR2RGB)
        
        if self.image is None:
            print('%s is not valid' % self.image_path)
            exit(0)

        self.image_resized = None
        
        
        # directorul cu imagini folosite pentru realizarea mozaicului
        self.small_images_dir = './../data/colectie/'
        
        # tipul imaginilor din director
        self.image_type = 'png'                
        
        # numarul de piese ale mozaicului pe orizontala
        self.num_pieces_horizontal = 25

        # pe verticala vor fi calcultate dinamic a.i sa se pastreze raportul        
        self.num_pieces_vertical = None
        
        # afiseaza piesele de mozaic dupa citirea lor
        self.show_small_images = False     
        
        # optiuni: 'aleator', 'caroiaj'
        self.layout = 'aleator'
        
        # pentru criteriul pozelor diferite (doar in cazul pentru caroiaj)
        self.different_small_images = False
        
        # criteriul dupa care se realizeaza mozaicul
        # optiuni: 'aleator', 'distantaCuloareMedie'        
        self.criterion = 'distantaCuloareMedie'         

        self.grayscale = False
        
        # daca params.layout == 'caroiaj', sa se foloseasca piese hexagonale        
        self.hexagon = False
        
        self.small_images = None
    
                       
            
            
            
            
            
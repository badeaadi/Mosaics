"""
    PROIECT MOZAIC
    
    Badea Adrian Catalin, grupa 334, anul III, FMI
"""

from parameters import *
import numpy as np
import pdb
import timeit


def mean_color(small_image):
    
    return np.mean(np.float32(small_image), (0, 1))



def euclidean_distance_best(params : Parameters, cropped_part, position):
        
    minimum_distance = math.inf
    mean_color_cropped_part = mean_color(np.float32(cropped_part))
    
    different_indices = []
    
    
    
    if params.different_small_images == True:
        row, col = position
        
        if params.hexagon == False:
            
            # print("Dreptunghiuri diferite")
            if row - 1 >= 0:
                different_indices.append(params.index_used[row - 1][col])
            
            if col - 1 >= 0:
                different_indices.append(params.index_used[row][col])
        else:
            
            # print("Hexagoane diferite")
            
            different_indices.append(params.index_used[row + 2][col])
            
            
            # Left and right row
            if row - 1 >= 0 and col - 1 >= 0:
                different_indices.append(params.index_used[row - 1][col - 1])
            
            if row - 1 >= 0:
                different_indices.append(params.index_used[row - 1][col + 1])
                        
            if col - 1 >= 0:
                different_indices.append(params.index_used[row + 1][col - 1])
            
            different_indices.append(params.index_used[row + 1][col + 1])
            if row - 2 >= 0:
                different_indices.append(params.index_used[row - 2][col])
            
    
    index = -1
        
    for i in range(0, params.small_images_np.shape[0]):
        distance = np.sum((mean_color_cropped_part - params.mean_color[i])**2)
        
        if distance < minimum_distance and (params.different_small_images == False or (i not in different_indices)):
            minimum_distance = distance 
            index = i
          
    return index
    
def add_pieces_grid(params: Parameters):
    
    start_time = timeit.default_timer()
    
    N, H, W, C = params.small_images.shape
    
    
    img_mosaic = np.zeros(params.image_resized.shape, np.uint8)
    
    h, w, c = params.image_resized.shape
    
    num_pieces = params.num_pieces_vertical * params.num_pieces_horizontal
    
    
    params.mean_color = np.zeros((params.small_images_np.shape[0],3), np.uint8)    
    
    if params.criterion == 'distantaCuloareMedie':
        
        for i in range(0, params.small_images_np.shape[0]):
            params.mean_color[i] = mean_color(params.small_images_np[i])

    if params.different_small_images == True:
         params.index_used = np.zeros((params.num_pieces_vertical, params.num_pieces_horizontal), np.int16)
    
    
    for i in range(params.num_pieces_vertical):
            for j in range(params.num_pieces_horizontal):
            
                
                axis0_max = min((i + 1) * H, h)
                axis1_max = min((j + 1) * W, w)
                
                if params.criterion == 'aleator':
                    
                    index = np.random.randint(low=0, high=N, size=1)
                
                elif params.criterion == 'distantaCuloareMedie':
                    
                    index  = euclidean_distance_best(params, params.image_resized[i * H: axis0_max, j * W: axis1_max, :], [i, j]) 
                    
                else:
                    print('Error! unknown option %s' % params.criterion)
                    exit(-1)   
                
                
                if params.different_small_images == True:
                    params.index_used[i][j] = index
                    
                img_mosaic[i * H: axis0_max, j * W: axis1_max,  :] = params.small_images_np[index, :, :, :]
                
                print('Building mosaic %.2f%%' % (100 * (i * params.num_pieces_horizontal + j + 1) / num_pieces))

       
        
    end_time = timeit.default_timer()
    print('Running time: %f s.' % (end_time - start_time))

    return img_mosaic



def add_pieces_random(params: Parameters):
    
    start_time = timeit.default_timer()
    
    
    params.mean_color = np.zeros((params.small_images_np.shape[0],3), np.uint8)    
    

    
    N, H, W, C = params.small_images.shape
    h, w, c = params.image_resized.shape
    
    img_mosaic = np.zeros((h + H, w + W, c), np.uint8)
    
    
    if params.criterion == 'distantaCuloareMedie':
        
        for i in range(0, params.small_images_np.shape[0]):
            params.mean_color[i] = mean_color(params.small_images_np[i])
    
    index_used = np.zeros((params.image_resized.shape[0] + W, params.image_resized.shape[1] + H), np.uint8)
    
    import random
    
    all_pixels = []
    for i in range(0, params.image_resized.shape[0]):
        for j in range(0, params.image_resized.shape[1]):
            all_pixels.append((i, j))
    
    print("Starting shuffling")
    random.shuffle(all_pixels)
    
    
    all_pixels_number = len(all_pixels)
    
    for k in range(0, len(all_pixels)):
        
        if k % 1000 == 0:
            print('Building mosaic %.3f%%' % (100 * k / all_pixels_number))
        
        i, j = all_pixels[k]
        
        
        # Verify written pixels
        if index_used[i][j] == 0:
            
            index = euclidean_distance_best(params, params.image_resized[i : i + H, j : j + W, :], [i, j])
            
            img_mosaic[i : i + H, j : j + W, :]  = params.small_images[index, :, :, :]
            index_used[i : i + H, j : j + W] = 1
            
            

    end_time = timeit.default_timer()
    print('Running time: %f s.' % (end_time - start_time))


    return img_mosaic[: h, : w, : ]


def add_pieces_hexagon(params: Parameters):
    
    
    N, H, W, C = params.small_images.shape
    h, w, c = params.image_resized.shape
    
    img_mosaic = np.zeros((h + H, w + W, c), np.uint8)
    
    params.mean_color = np.zeros((params.small_images_np.shape[0],3), np.uint8)   
    if params.criterion == 'distantaCuloareMedie':
        for i in range(0, params.small_images_np.shape[0]):
            params.mean_color[i] = mean_color(params.small_images_np[i])
    
    print(N, H, W, C)
    
    mask = np.zeros((H, W, 3), np.uint8)
    
    hexa_muchie = int(W / 3) + 1
    
    for i in range(H):
        for j in range(W):
            if (i + j >= hexa_muchie and W + H - i - j >= hexa_muchie and W + i - j >= hexa_muchie and H - i + j >= hexa_muchie):
                mask[i][j] = 1
    
    
    if params.different_small_images == True:
         params.index_used = np.zeros((params.num_pieces_vertical * 2 + 5, params.num_pieces_horizontal * 2 + 5), np.int16)
         params.index_used[:, :] = -1
    
    
    row = 1
    
    for i in range(int(H / 2), h, H) :
        col = 0
        for j in range(0, w, int(4 / 3 * W)):
            
            patch = params.image_resized[i : i + H, j : j + W, :]
            
            index = euclidean_distance_best(params, patch, [row, col])
            
            hexagon_small_image = np.multiply(params.small_images_np[index], mask)
            
            if params.different_small_images == True:
                params.index_used[row][col] = index
            
            img_mosaic[i : i + H, j : j + W, :] = hexagon_small_image
            
            col += 2
        
        row += 2
        
        
    print("Half done")
    
    row = 0
    
    for i in range(0, h, H) :
        col = 1
        
        for j in range(int(2 / 3 * W), w, int(4 / 3 * W)) :
            
            patch = params.image_resized[i : i + H, j : j + W, :]
            
            index = euclidean_distance_best(params, patch, [row, col])
            
            hexagon_small_image = np.multiply(params.small_images_np[index], mask)
            
            if params.different_small_images == True:
                params.index_used[row][col] = index
            
            img_mosaic[i : i + H, j : j + W, :] += hexagon_small_image
            
            col += 2
        
        row += 2

    return img_mosaic[H: h, W: w, : ]
    
                    
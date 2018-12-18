# -*- coding: utf-8 -*-
"""
Created on Wed Dec 12 15:27:22 2018

@author: BRIGHT
"""

def segmenter(pathToImage):
    
    """Handwritten segmentation algorithm
	
	Args:
		pathToImage: path to grayscale uint8 image of the text-line to be segmented.
				
	Returns:
		List of tuples and images. Each tuple contains the bounding box and the image of the segmented word.
	"""    
    
    import numpy as np
    
    import cv2
    
    import matplotlib.pyplot as plt
    
    def increase_image_contrast(pathToImage):
    
        img = cv2.imread(pathToImage, cv2.IMREAD_GRAYSCALE)

        # increase contrast
        pxmin = np.min(img)
        
        pxmax = np.max(img)
        
        imgContrast = (img - pxmin) / (pxmax - pxmin) * 255
        # increase line width
        kernel = np.ones((3, 3), np.uint8)
        
        imgCont = cv2.erode(imgContrast, kernel, iterations = 1)
        
        return imgCont
    
    imgCont = increase_image_contrast(pathToImage)
    
    img_new = imgCont
           
    tolerance = img_new.shape[0]*255-150
    
    sum_values = img_new.sum(axis=0)
    
    index = np.nonzero(sum_values > tolerance)
    
    index = index[0]
    
    def group_consecutive_numbers(vals, step = 1):
        
        """Return list of consecutive lists of numbers from vals (number list)."""
        
        run = []
        
        result = [run]
        
        expect = None
        
        for v in vals:
            
            if (v == expect) or (expect is None):
                
                run.append(v)
                
            else:
                
                run = [v]
                
                result.append(run)
                
            expect = v + step
            
        return result
    
    group_list = group_consecutive_numbers(index, step=1)
        
    length_of_list_in_list = []
    
    for i in range(len(group_list)):
        
        list_in_list = len(group_list[i])
        
        length_of_list_in_list.append(list_in_list)
        
    # find and return indexes of element in length_of_list_in_list > 1 
    
    def find_element_in_list(element, list_element):
        
        try:
            
            index_element = [i for i, x in enumerate(list_element) if x == element]
            
            return index_element
        
        except ValueError:
            
            return []
            
    element = 1
    
    index_element = find_element_in_list(element, length_of_list_in_list)
        
    if not index_element:
        
        final_index_list = []
        
        for k in range(len(group_list)):
                            
                index_value = np.min(group_list[k])
                
                final_index_list.append(index_value)
    else:
        
        group_list = [x for i, x in enumerate(group_list) if i not in index_element]
        
        final_index_list = []
        
        for k in range(len(group_list)):
                            
                index_value = np.min(group_list[k])
                
                final_index_list.append(index_value)
                
    def segment_image(img_new, final_index_list):
        
        idx = [0] + final_index_list + [img_new.shape[1]]
        
        segment = [img_new[:, start: end+1] for start, end in zip(idx, idx[1:])]
        
        return segment
    
    segment = segment_image(img_new, final_index_list)
    
    def save_splitted_images(segment):
        
        import os
        # check current working directory
        cwd = os.getcwd()
        
        image_directory = cwd + '\Images'
    
        try:  
            
            os.mkdir(image_directory)
            
        except OSError:  
            
            print ('Creation of the directory %s failed ' % image_directory)
            
        else:  
            
            print ('Successfully created the directory: %s ' % image_directory)
        
        import scipy.misc

        for l in range(len(segment)):
            
            filename = image_directory + '\data_%d.png'%(l,)
            
            scipy.misc.imsave(filename, segment[l])
    
    save_splitted_images(segment)
    
    def show_images(segment):
        
        for m in range(len(segment)):
            
            plt.subplot(1, len(segment), m+1)
            
            plt.imshow(segment[m], cmap = plt.get_cmap('gray'))
            
        return
    
    show_images(segment)
    
    return segment
    
        
        
        
        
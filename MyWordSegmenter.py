# -*- coding: utf-8 -*-
"""
Created on Thu Nov  8 15:55:52 2018

@author: BRIGHT
"""
def segmenter(pathToImage):
    """Handwritten segmentation algorithm proposed by Dr.Bright
	
	Args:
		pathToImage: path to grayscale uint8 image of the text-line to be segmented.
		
		
	Returns:
		List of tuples and images. Each tuple contains the bounding box and the image of the segmented word.
	"""    
    import numpy as np
    import cv2
    import matplotlib.pyplot as plt
    
    # Load image in grayscale
    img = cv2.imread(pathToImage)
    # Plot image in grayscale

    img_new = img[:,:,1]

    plt.imshow(img_new, cmap=plt.get_cmap('gray'))
           
    tolerance = img_new.shape[0]*255-14
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

    group_list=group_consecutive_numbers(index, step=1)
    
    final_index_list = []
    for k in range(len(group_list)):
        if len(group_list[k]) > 0:
            index_value = np.min(group_list[k])
        final_index_list.append(index_value)
         
    def split_image(img_new, final_index_list):
        idx = [0] + final_index_list + [img_new.shape[1]]
        segment = [img_new[:, start: end+1] for start, end in zip(idx, idx[1:])]
        return segment
    
    segment = split_image(img_new, final_index_list)
    
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
    return segment
        
        
        
        
# -*- coding: utf-8 -*-
"""
Created on Sat Mar 17 15:48:30 2018

@author: beran
"""

from IPython import get_ipython
get_ipython().run_line_magic('matplotlib', 'qt')

# Toto je důležité pro spuštění externího editoru sed3 i ginput
# %matplotlib qt

# conda install -c conda-forge -c mjirik imageio ffmpeg jupyter python=3.6 scikit-image
# conda create -n animalwatch -c conda-forge -c mjirik imageio ffmpeg jupyter python=3.6 scikit-image jupyter jupyter_contrib_nbextensions

import glob
import os.path as op
from pprint import pprint
import imageio
import skimage.color
import matplotlib.pyplot as plt
import numpy as np
import yaml

from collections import OrderedDict

def yaml_dump (filepath, data):
    #dumps data in a file
    with open(filepath, "w") as file_descriptor:
        yaml.dump(data, file_descriptor)
    print("Data dumped in", filepath )
   
def ginput2dict(ginput):
    dict = {}
    numOfPoints = ginput.__len__()
    for i in range (0,numOfPoints):
        for j in range (0,2):
            if j == 0:
                dict_key = "x" + str(i+1)
                dict[dict_key] = float(ginput[i][j])
            if j == 1:
                dict_key = "y" + str(i+1)
                dict[dict_key] = float(ginput[i][j])
    
    return dict

plt.ioff()


# datapath = ""
datapath = "../videaSP"
fnvideos = glob.glob(op.join(datapath, "*.AVI"))

#pprint(fnvideos)

allframes = None

# cislo videa 0-3
ivideo = 0
# pro krokovani videa
# videa jsou v 30 fps
step = 5

fn = fnvideos[ivideo]
print("video:", fn)

vid = imageio.get_reader(fn)

frame_size = vid.get_meta_data()["size"]
frame_number = vid.get_length()
#print("pocet snimku:", frame_number)
#print("velikost:", frame_size)

# priprava prazndeho pole pro snimky
allframes = np.zeros([int(frame_number / step), int(frame_size[1]), int(frame_size[0]), 3], dtype=np.uint8)
# print (allframes)

# loop nacte do prom image snimek z videa dle zadaneho kroku a umisti jej do matice allframes
for num in range(0, frame_number, step):
    image = vid.get_data(num)
#   print (num)
#   gray = skimage.color.rgb2gray(image)
    allframes[int(num/step), :, :, :] = image

# pocet snimku povodniho videa=900
# step = 5
# pocet snimku allframes = 180
#print (allframes.shape)

#bboxes = []

for i in range(127,129):
    bbox = {}
    frame_number = i
    plt.imshow(allframes[frame_number,...])# , cmap="gray")
    # left mouse button - add point
    # right mouse button - remove last point
    # middle mouse button - finish
    bbox = ginput2dict(plt.ginput(-1))
    #print (bbox)
    #bboxes.append(bbox)
    
    id = 1
    #bbox = {"x1": 41,
    #        "x2": 62,
    #        "y1": 187,
    #        "y2": 189,
    #            }
    bboxes = [bbox]

    data = {
        "path" : "cesta_k_souboru/video18.avi",
        "team" : ["Daniel Beran", "Hynek Marek"],
         "frames": {
            id: bboxes
        }
    }
    print (data)
    
    filepath = "test.yaml"
    yaml_dump(filepath, data)
    
    
    
#print (bboxes)



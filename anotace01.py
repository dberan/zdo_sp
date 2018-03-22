# -*- coding: utf-8 -*-
"""
Created on Sat Mar 17 15:48:30 2018

@author: beran
"""

#-------------------importy
from IPython import get_ipython
get_ipython().run_line_magic('matplotlib', 'qt')

import glob
import os.path as op
from pprint import pprint
import imageio
import skimage.color
import matplotlib.pyplot as plt
import numpy as np
import yaml

#-------------------ulozeni dat to souboru
#------------vstup: str filepath, str data    
#-----------vystup: ulozi do souboru a vypise, kam ulozil
def yaml_dump (filepath, data):
    #dumps data in a file
    with open(filepath, "w") as file_descriptor:
        yaml.dump(data, file_descriptor)
    print("Data dumped in", filepath )
    
#-------------------prevod ginputu do seznamu slovniku
#------------vstup: ginput z matalbu    
#-----------vystup: seznam, ktery obsahuje tolik slovniku, kolik je na snimku zviratek / bounding boxu
def ginput2listOfDict(ginput):
    mainDict = []
    numOfPoints = ginput.__len__()
    #print (numOfPoints)
    
    dict = {}
    for i in range (0,numOfPoints):  
        if i%2 == 0:
            dict = {}
            #print (dict)
        for j in range (0,2):
            if j == 0:
                dict_key = "x" + str((i%2)+1)    
                dict[dict_key] = int(round(ginput[i][j]))
            if j == 1:
                dict_key = "y" + str((i%2)+1)
                dict[dict_key] = int(round(ginput[i][j]))
                
        if i%2 == 1:
            mainDict.append(dict)
    
    #print (mainDict)
    return mainDict

plt.ioff()


datapath = "../videaSP"
fnvideos = glob.glob(op.join(datapath, "*.AVI"))

#pprint(fnvideos)

allframes = None

# cislo videa 0-3
ivideo = 3

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

#-------------------priprava prazndeho pole pro snimky
allframes = np.zeros([int(frame_number / step), int(frame_size[1]), int(frame_size[0]), 3], dtype=np.uint8)
# print (allframes)

#------------------- loop nacte do prom image snimek z videa dle zadaneho kroku a umisti jej do matice allframes
for num in range(0, frame_number, step):
    image = vid.get_data(num)
#   print (num)
#   gray = skimage.color.rgb2gray(image)
    allframes[int(num/step), :, :, :] = image

#-------------------slovnik pro snimky a jejich bboxy
frames = {}

for i in range(123,128):
    print ("frame: ", i)
    bboxesForFrame = []
    pseudo_frame_number = i
    plt.imshow(allframes[pseudo_frame_number,...])# , cmap="gray")
    
    bboxesForFrame = ginput2listOfDict(plt.ginput(-1))   
    
    #-------------------pokud existuje alespon jedno zviratko na snimku, uloz do slovniku
    #-------------------klic = cislo snimku ve videu; hodnota = seznam bboxu zviratek pro dany snimek
    if bboxesForFrame:
        frames[pseudo_frame_number*step] = bboxesForFrame

data = {
    "path" : fn,
    "team" : ["Daniel Beran", "Hynek Marek"],
        "frames": frames
}

filepath = "test.yaml"
yaml_dump(filepath, data)



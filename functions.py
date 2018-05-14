import numpy as np
import skimage
#import cv2 as cv
from skimage.morphology import dilation, erosion, square
import scipy
import yaml

def testFunc(string):
    print(string)
    
    
def hist(vstup):
    r = vstup.shape
    
    h = np.zeros(256)
    
    for i in range(0,r[0]):
        for j in range(0,r[1]):
            h[int(vstup[i,j])] += 1
    return h


def detektor_zmen_ve_snimku(vstup1,vstup2,px_vel):
        
    r = vstup1.shape
    rozl = [int(r[0]/px_vel),int(r[1]/px_vel)]
    
    zmenovy_rastr = np.zeros(rozl)
    for i in range(0,rozl[0]):
        for j in range(0,rozl[1]):
            seg1 = vstup1[i*px_vel:(i+1)*px_vel,j*px_vel:(j+1)*px_vel]
            seg2 = vstup2[i*px_vel:(i+1)*px_vel,j*px_vel:(j+1)*px_vel]
            
            h1 = hist(seg1)
            h2 = hist(seg2)
            zmenovy_rastr[i,j] = sum(abs(h1-h2))
            
    return zmenovy_rastr

def filtrace(snimek_zmen, prahova_hodnota, maska):
    
    #ret,th = cv.threshold(snimek_zmen,prahova_hodnota,255,cv.THRESH_BINARY)
    th = snimek_zmen>prahova_hodnota
#    ero = erosion(th, square(maska))
#    dil = dilation(ero, square(maska))
#    dil2 = dilation(dil, square(maska))
    
   
    
    fill = scipy.ndimage.morphology.binary_fill_holes(th)
    s = skimage.morphology.remove_small_objects(fill,20)
    poloprah = s*snimek_zmen
    med = skimage.filters.median(s, square(4))
    dil = dilation(s, square(maska))
    er = erosion(dil, square(maska))
    return s

def bboxy(inp,px):
    
    imlabel1 = skimage.measure.label(inp, background=0)
    pocet_objektu = np.max(imlabel1)
    bboxy = np.zeros((pocet_objektu,4)) 
    
    for i in range(1,pocet_objektu+1):
        objekt = (imlabel1==i).astype(int)
        dat = skimage.measure.regionprops(objekt)
        bboxy[i-1,:] = dat[0].bbox
    
    return bboxy*px


def ginput2listOfDict(ginput):
    mainDict = []
    numOfPoints = ginput.__len__()
    #print (numOfPoints)
    
    dict = {}
    for i in range (0,numOfPoints):  
        dict = {}
        for j in range (0,4):
            if j == 0:
                dict_key = "y1"   
            if j == 1:
                dict_key = "x1"
            if j == 2:
                dict_key = "y2"  
            if j == 3:
                dict_key = "x2"
            
            dict[dict_key] = int(round(ginput[i][j]))
                
        mainDict.append(dict)
    
    #print (mainDict)
    return mainDict


def yaml_dump (filepath, data):
    #dumps data in a file
    with open(filepath, "w") as file_descriptor:
        yaml.dump(data, file_descriptor)
    print("Data dumped in", filepath )
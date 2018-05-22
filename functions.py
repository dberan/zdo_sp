import numpy as np
import skimage
from skimage.morphology import dilation, erosion, square
import scipy
import yaml
   
#funkce pro vytvoreni histogramu ze vstupniho snimku    
def hist(vstup):
    r = vstup.shape
    
    h = np.zeros(256)
    
    for i in range(0,r[0]):
        for j in range(0,r[1]):
            h[int(vstup[i,j])] += 1
    return h



#funkce pro vytvoreni snimku zmen
def detektor_zmen_ve_snimku(pozadi,snimek,px_vel):
    
    #rozliseni vstupnich obrazu    
    r = pozadi.shape
    rozl = [int(r[0]/px_vel),int(r[1]/px_vel)]
    
    #matice nul pro ulozeni zmenovych hodnot
    zmenovy_rastr = np.zeros(rozl)
    
    #vyhodnoceni zmen pro jednotlive segmenty
    for i in range(0,rozl[0]):
        for j in range(0,rozl[1]):
            seg1 = pozadi[i*px_vel:(i+1)*px_vel,j*px_vel:(j+1)*px_vel]
            seg2 = snimek[i*px_vel:(i+1)*px_vel,j*px_vel:(j+1)*px_vel]
            
            h1 = hist(seg1)
            h2 = hist(seg2)
            zmenovy_rastr[i,j] = sum(abs(h1-h2))
            
    return zmenovy_rastr


#segmentace a filtrace snimku zmen
def filtrace(snimek_zmen, prahova_hodnota, maska):
    
    #segmentace
    th = snimek_zmen > prahova_hodnota
    
    #vypleneni der
    fill = scipy.ndimage.morphology.binary_fill_holes(th)
    
    #filtrace malych objektu
    s = skimage.morphology.remove_small_objects(fill,15)
    
    #uzavreni
    dil = dilation(s, square(maska))
    er = erosion(dil, square(maska))
    
    return er


#vytvoreni bounding boxu
def bboxy(inp,px):
    
    #label jednotlivych objektu
    imlabel1 = skimage.measure.label(inp, background=0)
    
    pocet_objektu = np.max(imlabel1)
    
    #matice pro ulozeni vsech bounding boxu
    bboxy = np.zeros((pocet_objektu,4)) 
    
    #matice pro ulozeni filtrovanych bounding boxu
    bboxy_filter = []
    
    #ulozeni bounding boxu vsech objektu do matice bboxy
    for i in range(1,pocet_objektu+1):
        objekt = (imlabel1==i).astype(int)
        dat = skimage.measure.regionprops(objekt)
        bboxy[i-1,:] = dat[0].bbox
        
    #odstraneni bounding boxu, ktery lezi uvnitr jineho 
    for m in range(1,pocet_objektu+1):
        uvnitr = False
        for n in range(1,pocet_objektu+1):
            if (m!=n and (bboxy[m-1][0] >= bboxy[n-1][0]) and (bboxy[m-1][1] >= bboxy[n-1][1]) and (bboxy[m-1][2] <= bboxy[n-1][2]) and (bboxy[m-1][3] <= bboxy[n-1][3])):
                uvnitr = True
        if not uvnitr:
            bboxy_filter.append([px*bboxy[m-1][0],px*bboxy[m-1][1],px*bboxy[m-1][2],px*bboxy[m-1][3]])
            
    return bboxy_filter



def ginput2listOfDict(ginput):
    mainDict = []
    numOfPoints = ginput.__len__()
    sl = ["y1","x1","y2","x2"]
    
    dict = {}
    for i in range (0,numOfPoints):  
        dict = {}
        for j in range (0,4):
                        
            dict[sl[j]] = int(round(ginput[i][j]))
                
        mainDict.append(dict)
    
    return mainDict


def yaml_dump (filepath, data):
    #dumps data in a file
    with open(filepath, "w") as file_descriptor:
        yaml.dump(data, file_descriptor)
    print("Data dumped in", filepath )
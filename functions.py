import numpy as np
import skimage

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




def bboxy(inp):
    
    imlabel1 = skimage.measure.label(inp, background=0)
    pocet_objektu = np.max(imlabel1)
    bboxy = np.zeros((pocet_objektu,4)) 
    
    for i in range(1,pocet_objektu+1):
        objekt = (imlabel1==i).astype(int)
        dat = skimage.measure.regionprops(objekt)
        bboxy[i-1,:] = dat[0].bbox
    
    return bboxy
from IPython import get_ipython
get_ipython().run_line_magic('matplotlib', 'qt')

import glob
import os.path as op
import imageio
import skimage.color
import matplotlib.pyplot as plt
import numpy as np
import scipy
import scipy.ndimage
from skimage import morphology
import skimage.io
from skimage.feature import local_binary_pattern


def bboxy(inp):
    #vstupem je naprahovany boolean obrazek
    imlabel1 = skimage.measure.label(inp, background=0)
    pocet_objektu = np.max(imlabel1)
    bboxy = np.zeros((pocet_objektu,4)) 
    
    for i in range(1,pocet_objektu+1):
        objekt = (imlabel1==i).astype(int)
        dat = skimage.measure.regionprops(objekt)
        bboxy[i-1,:] = dat[0].bbox
    
    return bboxy



#určite je pro histogram nějaká funkce, ale neměl jsem zrovna připojení na to to vygooglit když jsem to dělal
def hist(vstup):
    r = vstup.shape
    
    h = np.zeros(256)
    
    for i in range(0,r[0]):
        for j in range(0,r[1]):
            h[int(vstup[i,j])] += 1
    return h





def detektor(vstup1,vstup2,px_vel):
    
    r = vstup1.shape
    rozl = [int(r[0]/px_vel),int(r[1]/px_vel)]
    
    vystup = np.zeros(rozl)
    for i in range(0,rozl[0]):
        for j in range(0,rozl[1]):
            seg1 = vstup1[i*px_vel:(i+1)*px_vel,j*px_vel:(j+1)*px_vel]
            seg2 = vstup2[i*px_vel:(i+1)*px_vel,j*px_vel:(j+1)*px_vel]
            #h1 = np.histogram(seg1, bins = range(256))
            #h2 = np.histogram(seg2, bins = range(256))
            #vystup[i,j] = sum(abs(h1[0]-h2[0]))
            
            h1 = hist(seg1)
            h2 = hist(seg2)
            vystup[i,j] = sum(abs(h1-h2))
            
    return vystup
    





plt.ioff()


datapath = "../videaSP"
fnvideos = glob.glob(op.join(datapath, "*.AVI"))


allframes = None

ivideo = 9
step = 1

fn = fnvideos[ivideo]
print("video:", fn)

vid = imageio.get_reader(fn)

frame_size = vid.get_meta_data()["size"]
frame_number = vid.get_length()


#allframes = np.zeros([int(frame_number / step), int(frame_size[1]), int(frame_size[0]), 3], dtype=np.uint8)




#poz = skimage.color.rgb2gray(vid.get_data(500))
poz = skimage.io.imread('..\pozadi\V__00014_xvid_poz.jpg')
akt = skimage.color.rgb2gray(vid.get_data(30))





m = 'default'
#poz_lbp = lbp(poz)
poz_lbp = local_binary_pattern(poz,8,2,method=m)
print("---")
#akt_lbp = lbp(akt)
akt_lbp = local_binary_pattern(akt,8,2,method=m)
print("---")

test_puv = detektor(poz_lbp,akt_lbp,10)>130
test = skimage.morphology.opening(test_puv)
test = skimage.morphology.closing(test)
plt.imshow(test_puv)
plt.show()
print(bboxy(test_puv))
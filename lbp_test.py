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



def lbp(inp):
    rozmer = inp.shape
    lbp_im = np.zeros([rozmer[0],rozmer[1]])
    
    for i in range(1,rozmer[0]-1):
        for j in range(1,rozmer[1]-1):
            centrum = inp[i,j]
            sousedi = [inp[i-1,j-1],inp[i-1,j],inp[i-1,j+1],inp[i,j-1],inp[i,j+1],inp[i+1,j-1],inp[i+1,j],inp[i+1,j+1]]
            nasobky = [1,2,4,8,16,32,64,128]
            
            for k in range(0,8):
                if(sousedi[k] >= centrum):
                    lbp_im[i,j] += nasobky[k]

    return lbp_im



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
            h1 = hist(seg1)
            h2 = hist(seg2)
            vystup[i,j] = sum(abs(h1-h2))
    return vystup
    





plt.ioff()


datapath = "../videaSP"
fnvideos = glob.glob(op.join(datapath, "*.AVI"))


allframes = None

ivideo = 0
step = 1

fn = fnvideos[ivideo]
print("video:", fn)

vid = imageio.get_reader(fn)

frame_size = vid.get_meta_data()["size"]
frame_number = vid.get_length()


#allframes = np.zeros([int(frame_number / step), int(frame_size[1]), int(frame_size[0]), 3], dtype=np.uint8)




poz = skimage.color.rgb2gray(vid.get_data(500))
akt = skimage.color.rgb2gray(vid.get_data(650))




poz_lbp = lbp(poz)
print("---")
akt_lbp = lbp(akt)
print("---")



test = detektor(poz_lbp,akt_lbp,10)
plt.imshow(test)
plt.show()

import functions
import glob
import os.path as op
import imageio
import skimage
import skimage.io
from skimage.feature import local_binary_pattern
import matplotlib.pyplot as plt
import time


#prozatim jsem doplnil spusteni funkci ze sveho testovaciho souboru.

#datapath = "../videaSP"
datapath  = "C:/Beran_Daniel_files/FAV/_2017_2018/ZDO_SP/videa"
#fnvideos = glob.glob(op.join(datapath, "*.AVI"))
fnvideos = glob.glob(op.join(datapath, "IMAG0050.AVI"))

allframes = None

ivideo = 0
step = 1

fn = fnvideos[ivideo]
print("video:", fn)

vid = imageio.get_reader(fn)

frame_size = vid.get_meta_data()["size"]
frame_number = vid.get_length()


#allframes = np.zeros([int(frame_number / step), int(frame_size[1]), int(frame_size[0]), 3], dtype=np.uint8)


#poz = skimage.io.imread('..\pozadi\V__00014_xvid_poz.jpg')
poz = skimage.io.imread('C:/Beran_Daniel_files/FAV/_2017_2018/ZDO_SP/pozadi/IMAG_0050_poz.jpg')
akt = skimage.color.rgb2gray(vid.get_data(780))

m = 'default'
poz_lbp = local_binary_pattern(poz,8,2,method=m)
akt_lbp = local_binary_pattern(akt,8,2,method=m)

#parametr px_vel zadavat jenom v hodnotach spolecneho delitele 720, 1280 (rozliseni obrazu)
snimek_zmen = functions.detektor_zmen_ve_snimku(poz_lbp,akt_lbp,10)

filtr = functions.filtrace(snimek_zmen, 120, 3)

plt.imshow(akt, cmap='gray')
plt.imshow(filtr, cmap='cool', alpha=0.2, extent =[0,1280,720,0])

plt.show()
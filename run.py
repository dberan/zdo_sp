import functions
import glob
import os.path as op
import imageio
import skimage
import skimage.io
from skimage.feature import local_binary_pattern
import matplotlib.pyplot as plt

functions.testFunc('test')




    #prozatim jsem doplnil spusteni funkci ze sveho testovaciho souboru.
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


poz = skimage.io.imread('..\pozadi\V__00014_xvid_poz.jpg')
akt = skimage.color.rgb2gray(vid.get_data(30))


m = 'default'
poz_lbp = local_binary_pattern(poz,8,2,method=m)
akt_lbp = local_binary_pattern(akt,8,2,method=m)

#parametr px_vel zadavat jenom v hodnotach spolecneho delitele 720, 1280 (rozliseni obrazu)
test = functions.detektor_zmen_ve_snimku(poz_lbp,akt_lbp,20)

plt.imshow(test)
plt.show()
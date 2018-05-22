import skimage
import skimage.io
import imageio
import glob
import os.path as op

datapath  = "../videaSP"
fnvideos = glob.glob(op.join(datapath, "IMAG0028.AVI"))
fn = fnvideos[0]
vid = imageio.get_reader(fn)

frame_size = vid.get_meta_data()["size"]
frame_number = vid.get_length()

for i in range(0,frame_number):
    if i == 0:
        avr_frame = skimage.color.rgb2gray(vid.get_data(i))
        print (i)
    else:
        avr_frame = avr_frame + skimage.color.rgb2gray(vid.get_data(i))
        print(i)

print('Suma vypoctena')   

avr = avr_frame / frame_number

print('Prumer vypocten')    

skimage.io.imsave('IMAG0028_AVR.png',avr)

print('Soubor ulozen') 
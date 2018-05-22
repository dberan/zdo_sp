import functions
import glob
import os.path as op
import imageio
import skimage
import skimage.io
from skimage.feature import local_binary_pattern
import matplotlib.pyplot as plt


datapath = "../videaSP"

video_nazev = "IMAG0063"
prah = 130

#datapath  = "C:/Beran_Daniel_files/FAV/_2017_2018/ZDO_SP/videa"
#fnvideos = glob.glob(op.join(datapath, "*.AVI"))
fnvideos = glob.glob(op.join(datapath, video_nazev + ".AVI"))

allframes = None


#nacteni videa
fn = fnvideos[0]
print("video:", fn)

vid = imageio.get_reader(fn)

frame_number = vid.get_length()


#nacteni snimku pozadi
poz = skimage.io.imread("../pozadi/" + video_nazev + "_poz.jpg")

#LBP snimku pozadi
poz_lbp = local_binary_pattern(poz,8,2,method="default")



frames = {}
for i in range(0,5):
    print("snimek c. " + str(i))
    
    #vyber aktualniho snimku
    akt = skimage.color.rgb2gray(vid.get_data(i))
    akt_lbp = local_binary_pattern(akt,8,2,method="default")
    
    #nalezeni zmenoveho snimku
    snimek_zmen = functions.detektor_zmen_ve_snimku(poz_lbp,akt_lbp,10)
    
    #filtrace zmen
    filtr = functions.filtrace(snimek_zmen, prah, 3)
      
    #vygenerovani bounding boxu
    bboxesForFrame = functions.ginput2listOfDict(functions.bboxy(filtr,10))   
    
    #ulozeni bounding boxu v pripade, ze byly nejake nalezeny    
    if bboxesForFrame:
        frames[i] = bboxesForFrame
    

#ulozeni vysledku do souboru .yaml
data = {
    "path" : video_nazev + ".avi",
    "team" : ["Daniel Beran", "Hynek Marek"],
        "frames": frames
}

filepath = video_nazev + ".yaml"
functions.yaml_dump(filepath, data)




import cv2
import yaml
import time

#porovnavane video
videoString = 'IMAG0028'

#YAML s automatickou identifikaci
with open(".../vysledky_ZDO/"+videoString+".yaml", 'r') as stream1:
    try:
        yamlFile1 = yaml.load(stream1)
    except yaml.YAMLError as exc:
        print(exc)        
frames1 = yamlFile1['frames']

#YAML s rucni identifikaci
with open(".../anotace/IMAG0050.yaml", 'r') as stream2:
    try:
        yamlFile2 = yaml.load(stream2)
    except yaml.YAMLError as exc:
        print(exc)
        
frames2 = yamlFile2['frames']

#nacteni videa
cap = cv2.VideoCapture('.../videa/'+videoString+'.AVI')
curr_frame = 0

while(cap.isOpened()):
    #pro zmenu rychlosti prehravani
    time.sleep(0.02)
    ret, img = cap.read()
    
    if curr_frame in frames1.keys():
        frame1 = frames1[curr_frame]    
        num_of_bbox1 = len(frame1)
        for i in range(0,num_of_bbox1):
            bbox1 = frame1[i]    
            x11 = bbox1['x1']
            y11 = bbox1['y1']
            x21 = bbox1['x2']
            y21 = bbox1['y2']
            cv2.rectangle(img,(x11,y11),(x21,y21),(0,0,255),2)
            
    if curr_frame in frames2.keys():
        frame2 = frames2[curr_frame]    
        num_of_bbox2 = len(frame2)
        for i in range(0,num_of_bbox2):
            bbox2 = frame2[i]    
            x12 = bbox2['x1']
            y12 = bbox2['y1']
            x22 = bbox2['x2']
            y22 = bbox2['y2']
            cv2.rectangle(img,(x12,y12),(x22,y22),(0,255,0),2)
    
    cv2.imshow('frame',img)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    
    curr_frame = curr_frame + 1
    
cap.release()
cv2.destroyAllWindows()
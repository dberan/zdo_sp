# -*- coding: utf-8 -*-
"""
Created on Sun Mar 18 09:37:55 2018

@author: beran
"""

tuples = [(763.3709677419354, 546.8806451612902), (820.1451612903224, 613.9774193548386),(820.1451612903224, 613.9774193548386),(820.1451612903224, 613.9774193548386)]

def ginput2dict(ginput):
    dict = {}
    numOfPoints = ginput.__len__()
    for i in range (0,numOfPoints):
        for j in range (0,2):
            if j == 0:
                dict_key = "x" + str(i+1)
                dict[dict_key] = tuples[i][j]
            if j == 1:
                dict_key = "y" + str(i+1)
                dict[dict_key] = tuples[i][j]
        
    
    return dict

bbox = ginput2dict(tuples)

print (bbox)
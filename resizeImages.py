# Script for finding image height and width that keep aspect ratio
# then updates all html files to use updated size with maximum width
import os 
import cv2
import numpy as np
import matplotlib.pyplot as plt
# read image
# read size if found
# resize read html file and modify the size 
# 
print("Image properties updater ...") 
arxV = "v3.9.1"
imgFolder = os.path.join("help", arxV, "img")  
imgFolders = os.listdir(imgFolder)
maxWidth= 570  

# Get all html files 
webFolder = os.path.join("help", arxV)  
webFnms = []
for root, dirs, files in os.walk(webFolder):
    for file in files:
        #append the file name to the list
        if (".html" in file):
           webFnms.append(os.path.join(root,file))


# get reduced image size with correct aspect ratio
def getImageNewSize(imgShape, maxWidth):
    # reduce image size 10% each time until we reach maxwidth
    imgH, imgW = imgShape
    while imgW >maxWidth:
        # reduce 
        imgH= int(imgH-imgH*(0.1))
        imgW= int(imgW-imgW*(0.1))
        #print(imgW,imgH)
    return imgH, imgW


imgLst = []
# Resize images
for imgF in imgFolders:
    fnms = os.listdir(os.path.join(imgFolder,imgF))   
    for fnm in fnms:
        imgPath = os.path.join(imgFolder, imgF, fnm)
        #print(imgPath)
        img = cv2.imread(imgPath, 0)        
        # Resize for maximum width
        #print(img.shape[1],img.shape[0])
        imgH, imgW = getImageNewSize(img.shape,maxWidth)
        #print(imgW, imgH)  
        # update the webpage with the new reduced size
        imgLst.append([fnm, imgW, imgH])
        #plt.imshow(img, cmap='gray')          


def updateWebPage(line, imgRecord):
    newLinePart = 'width="'+str(imgRecord[1])+'" height="'+str(imgRecord[2])+'" /> \n'
    lineStart=line.find('width="')
    newLine = line[:lineStart] + newLinePart 
    return newLine

# Update all webpages  and change image sizes
for webF in webFnms:
    # open the webpage as text file 
    with open(webF,'r') as f1, open('tmp.html', 'w') as f2:
            lines = f1.readlines()
            for line in lines:
                if "<img src=" in line:
                # get this image size
                    for imgRecord in imgLst:
                        if imgRecord[0] in line:
                           line= updateWebPage(line, imgRecord)
                f2.write(line)
    os.remove(webF)              
    os.rename('tmp.html',webF)      
print("done! "+str(len(webFnms)) +" html files are updated! ")
import argparse
import random
import time
import numpy as np
import cv2
import sys

from pythonosc import udp_client

#ip=sys.argv[1]
#print ("ip:",ip)
def fadeIn (img1, img2): #pass images here to fade between
        #while True:
        for IN in range(45,50,1):
                fadein = IN/150.0
                dst = cv2.addWeighted( img1, fadein, img2, fadein, 0) #linear $
                cv2.imshow('window', dst)
                cv2.waitKey(1)
#                print ("fadein:",fadein)
#                time.sleep(0.01)
#                if fadein == 0.5: #blendmode mover
#                        fadein = 0.5
        return # exit function
        
def image_resize(image, width = None, height = None, inter = cv2.INTER_AREA):
    # initialize the dimensions of the image to be resized and
    # grab the image size
    dim = None
    (h, w) = image.shape[:2]

    # if both the width and height are None, then return the
    # original image
    if width is None and height is None:
        return image

    # check to see if the width is None
    if width is None:
        # calculate the ratio of the height and construct the
        # dimensions
        r = height / float(h)
        dim = (int(w * r), height)

    # otherwise, the height is None
    else:
        # calculate the ratio of the width and construct the
        # dimensions
        r = width / float(w)
        dim = (width, int(h * r))

    # resize the image
    resized = cv2.resize(image, dim, interpolation = inter)

    # return the resized image
    return resized
    
def getPicGazeHead():
  print ("getPicGazeHead")
  f = open('gaze_nasa_valid_result.txt','r')
  gazeHeadDict = {}
  for r in f:
    print(r)
    token = r.split(" ")

#    for i in range(len(token)):
#        print (str(i)+" "+token[i])

    picFileName = token[0]
    headPoseYaw = float(token[15].replace("[","").replace(",",""))
    headPosePitch=float(token[16].replace(",",""))
    headPoseRoll =float(token[17].replace(",","").replace("]",""))  
    
    gazeVectorX = float(token[6].replace(",","").replace("[",""))
    gazeVectorY = float(token[7].replace(",",""))
    gazeVectorZ = float(token[8].replace(",","").replace("]",""))
    
#    gazeHeadTuple = (headPoseYaw, headPosePitch, headPoseRoll, gazeVectorX, gazeVectorY, gazeVectorZ)
    gazeHeadTuple = (headPoseYaw, headPosePitch, headPoseRoll, gazeVectorX, gazeVectorY, gazeVectorZ)
    gazeHeadDict[picFileName] = gazeHeadTuple

#  print (gazeHeadDict)
  return gazeHeadDict;
    
    
if __name__ == "__main__":
  parser = argparse.ArgumentParser()
  parser.add_argument("--ip", default="192.168.88.199",
      help="The ip of the OSC server")
  parser.add_argument("--port", type=int, default=12000,
      help="The port the OSC server is listening on")
  args = parser.parse_args()

  client = udp_client.SimpleUDPClient(args.ip, args.port)

  headToken=""
  gazeToken=""
  headT=""
  gazeT=""
  
  picGazeHeadDict = getPicGazeHead()
  oldFileName=""
  with open('test.txt') as f:
    f.seek(0,2)
    isHead=False
    isGaze=False
    validCount=0
    while True:
      last_pos = f.tell()
      line = f.readline()
      if line:
        if (line.find("Head")!=-1):
#          print (line)
          headToken=line
          headT=line.split(":")[1]
          hs = headT.split("[")[1].replace("]","").strip()
          hx = float(hs.split(",")[0].strip())
          hy = float(hs.split(",")[1].strip())
          hz = float(hs.split(",")[2].strip())
          
#          print ("headT:",headT)
#          print ("hs:",hs)
#          print (hx)
#          print (hy)
#          print (hz)
          
          isHead = True
        if (line.find("Gaze")!=-1):
#          print (line)
          gazeToken=line
          gazeT=line.split(":")[1]
          gs = headT.split("[")[1].replace("]","").strip()

          gx = float(gs.split(",")[0].strip())
          gy = float(gs.split(",")[1].strip())
          gz = float(gs.split(",")[2].strip())

          isGaze = True
#          print ("gazeT:",gazeT)
#          print ("gs:",gs)
#          print (gx)
#          print (gy)
#          print (gz)
          
        if (isHead and isGaze):
          minDistance=999999999
          minPicFileName=""
          validCount+=1
#          print ("validCount:",validCount)
          if (validCount%200==0):
            for k,v in picGazeHeadDict.items():
    #            print (k)
    #            print (v)
            
              hDist = (hx-v[0])**2+(hy-v[1])**2+(hz-v[2])**2
              gDist = (gx-v[3])**2+(gz-v[4])**2+(gz-v[5])**2
              total = hDist*gDist
    #            print ("total:",total)

              if (total<minDistance):
                  minPicFileName = k
                  minDistance=total
    #            print ("minDistance:",minDistance)
            
#            print ("minPicFileName:",minPicFileName,"minDistance:",minDistance)
            imgFile = minPicFileName.replace(".mp4.txt","")
            print ("imgFile:",imgFile)
#            imgFileName = '.\\MET_art_allJPGNew\\allJPGNew\\200_'+imgFile
#            imgFileName = '.\\finalOriginJPG\\finalOriginJPG-400\\'+imgFile
            imgFileName = '.\\nasa2020\\png\\png\\'+imgFile

#            imgFileName = '.\\NPM_new2jpg2mp4resize\\new2jpg2mp4resize\\'+imgFile
            client.send_message("/filter", imgFile)
#            print ("imgFileName:",imgFileName)
            if (oldFileName!=""):
                img1 = cv2.imread(imgFileName)
#                img2 = cv2.imread(oldFileName)
#                imgResize1 = image_resize(img1, width=1070,height = 1910)
#                imgResize2 = image_resize(img2, width=1070,height = 1910)
#                imgResize1 = cv2.resize(img1, (480,720))
#                imgResize2 = cv2.resize(img2, (480,720))
                try:
                  imgResize1 = cv2.resize(img1, (360,540))
#                  imgResize2 = cv2.resize(img2, (360,540))
#                  fadeIn(imgResize2, imgResize1)
                  cv2.imshow('window', imgResize1)
                  cv2.waitKey(1)		
  
                except Exception as R:
                  continue


#            img = cv2.imread(imgFileName)
            oldFileName = imgFileName
            
#            imgResize = image_resize(img, width=1070,height = 1910)
#            cv2.imshow('gaze',imgResize)

#            time.sleep(5)
#            print ("hi")
            cv2.waitKey(1)
    #          client.send_message("/filter", random.random())
#           client.send_message("/filter", minPicFileName)
#            client.send_message("/filter", imgFile)
          
#            print(ghTuple)
            
#    for x in range(10):
#      client.send_message("/filter", random.random())
#      time.sleep(1)
      
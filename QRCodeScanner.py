import cv2
import os
import re
from PIL import Image
from pyzbar.pyzbar import decode

def sorted_alphanumeric(data):
    convert = lambda text: int(text) if text.isdigit() else text.lower()
    alphanum_key = lambda key: [ convert(c) for c in re.split('([0-9]+)', key) ] 
    return sorted(data, key=alphanum_key)

def makeFolder(videoFileName):
    folderName = "./"+os.path.splitext(videoFileName)[0]
    if not os.path.exists(folderName):
        os.mkdir(folderName)
    os.chdir(folderName)

videoFileName = "ScanQRCodeTest.MOV"
FRAME_INTERVAL = 1

vidcap = cv2.VideoCapture(videoFileName)

makeFolder(videoFileName)

fps = vidcap.get(cv2.CAP_PROP_FPS)      # OpenCV2 version 2 used "CV_CAP_PROP_FPS"
frame_count = int(vidcap.get(cv2.CAP_PROP_FRAME_COUNT))
duration = frame_count/fps
success,image = vidcap.read()
count = 0
while success:
    vidcap.set(cv2.CAP_PROP_POS_MSEC,(count*(1000/(fps*FRAME_INTERVAL))))
    cv2.imwrite("Frame%d.jpg" % count, image)     # save frame as JPEG file      
    print("Saved {}".format(count))
    success,image = vidcap.read()
    #print('Read a new frame: ', success)
    count += 1

def pyzbarDecode(imgPath):
    result = decode(Image.open(imgPath))
    for barcode in result:
        return(barcode.data.decode("utf-8"))

#Running the check
hasValueCountcv2 = 0
hasValueCtpyzBar = 0
for imageFrame in sorted_alphanumeric(os.listdir(".")):
    img = cv2.imread(imageFrame)
    detect = cv2.QRCodeDetector()
    value, points, straight_qrcode = detect.detectAndDecode(img)
    if not value == "":
        print("CV2 -- " + imageFrame + "\t-\t" + value)
        hasValueCountcv2+=1
    pzBarData = pyzbarDecode(imageFrame)
    if pzBarData:
        print("PYZBAR -- " + imageFrame + "\t-\t" + pzBarData)
        hasValueCtpyzBar+=1


checkingFrameCt = round(duration*1000/(fps*FRAME_INTERVAL))
print("-"*40)
print("Frame Rate:\t\t\t{}\nDuration:\t\t\t{} sec".format(round(fps, 5), duration))
print("TotalFrames:\t\t\t{}".format(round(duration*1000/fps)))
print("Number of frames checking:\t{} (Saving every {} frame)".format(checkingFrameCt, FRAME_INTERVAL))
print("CV2 Positive Scans:\t\t{}\nCV2 Percantage Working:\t\t{}%".format(hasValueCountcv2, round(hasValueCountcv2/checkingFrameCt*100))) #out of checking
print("PYZBAR Positive Scans:\t\t{}\nPYZBAR Percantage Working:\t{}%".format(hasValueCtpyzBar, round(hasValueCtpyzBar/checkingFrameCt*100))) #out of checking
print("-"*40)


#print("Frame Rate:\t\t{}\nDuration:\t\t{} sec\nTotalFrames:\t\t{}".format(round(fps, 5), duration, round(fps*duration)))
#print("Checking Total Frames:\t{} (Saving every {} frame)".format(checkingFrameCt, FRAME_INTERVAL/1000))


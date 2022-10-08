import qrcode
import os 
import pandas as pd
from PIL import ImageDraw, ImageFont


df = pd.read_excel('ActionDescriptionsShortened.xlsx')
data = df.to_numpy()

font = ImageFont.truetype(".Fonts/TimesNewRomanBold.ttf", size=40)

def camelCase(st):
    output = ''.join(x for x in st.title() if x.isalnum())
    return output[0].lower() + output[1:]


folderName = "./QRPics/"
if not os.path.exists(folderName):
    os.mkdir(folderName)
os.chdir(folderName)

actionCount = 0
for action in data:
    qr = qrcode.QRCode(
        version=5,                                          #Dimension of QR Code
        error_correction=qrcode.constants.ERROR_CORRECT_H,  #About 30% or less errors can be corrected. (Max)
        box_size=20,                                        #Num of pixels each box is 
        border=3,                                           #How many boxes make up size of border
    )

    if not action[2] == "-":
        QRCodeData = action[0] + " - " + action[2]
        fileName = str(actionCount) + "_" + camelCase(action[0] + " " + action[2]) + ".png"
    else:
        QRCodeData = action[0]
        fileName = str(actionCount) + "_" + camelCase(action[0]) + ".png"

    qr.add_data(QRCodeData)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")

    drawImg = ImageDraw.Draw(img)
    
    #drawImg.text((0,0), "TEST", size=20)
    drawImg.text((img.size[0]/2 - font.getsize(QRCodeData)[0]/2, 
            img.size[1]-font.getsize(QRCodeData)[1]*1.25), QRCodeData, font=font)
    #img.size[0]/2, img.size[1]*0.9


    img.save(fileName)
    actionCount+=1

    print("Saved QR Code {} out of {}".format(actionCount, len(data)))
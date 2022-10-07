import qrcode
import os 
import pandas as pd

df = pd.read_excel('ActionDescriptions.xlsx')
data = df.to_numpy()

def camelCase(st):
    output = ''.join(x for x in st.title() if x.isalnum())
    return output[0].lower() + output[1:]


folderName = "./QRPics/"
if not os.path.exists("./QRPics/"):
    os.mkdir("./QRPics/")
os.chdir("./QRPics/")

actionCount = 0
for action in data:
    qr = qrcode.QRCode(
        version=5,                                          #Dimension of QR Code
        error_correction=qrcode.constants.ERROR_CORRECT_H,  #About 30% or less errors can be corrected.
        box_size=30,                                        #Num of pixels each box is 
        border=2,                                           #How many boxes make up size of border
    )
    if not action[2] == "-":
        QRCodeData = action[0] + "--" + action[2]
        fileName = str(actionCount) + "_" + camelCase(action[0] + " " + action[2]) + ".png"
    else:
        QRCodeData = action[0]
        fileName = str(actionCount) + "_" + camelCase(action[0]) + ".png"

    qr.add_data(QRCodeData)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")
    img.save(fileName)
    actionCount+=1

    print("Saved QR Code {} out of {}".format(actionCount, len(data)))
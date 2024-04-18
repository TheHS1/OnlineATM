import cv2
import easyocr

def getCheckInfo(path):
    img = cv2.imread(path)
    height, width, channels = img.shape
    reader = easyocr.Reader(['en'], gpu=False, verbose=False)

    bounds = [  
                [
                    [0, 0], [int(height*0.3), int(width*0.37)]
                ], # name address
                [
                    [0, int(width*0.71)], [int(height*0.3), width]
                ], # date
                [
                    [int(height*0.27), int(width*0.76)], [int(height*0.47), int(width*0.93)]
                ], # numerical
                [
                    [int(height*0.52), int(width*0.04)], [int(height*0.67), int(width*0.77)]
                ], # spelled
                [
                    [int(height*0.28), int(width*0.15)], [int(height*0.53), int(width*0.75)]
                ], # Recipient
                [
                    [int(height*0.73), int(width*0.14)], [int(height*0.88), int(width*0.45)]
                ],  # Memo
                [
                    [int(height*0.88), int(width*0.05)], [int(height), int(width*0.5)]
                ]  # sender_account
             ]

    labels = ["sender_info", 
              "date", 
              "numerical_amount", 
              "spelled_amount", 
              "recipient", 
              "memo",
              "sender_account"
             ]

    data = {}

    for i, bound in enumerate(bounds):
        text = reader.readtext(img[bound[0][0]:bound[1][0], bound[0][1]:bound[1][1]])
        data[labels[i]] = ' '.join(line[1] for line in text)

    return data

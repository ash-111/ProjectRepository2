import matplotlib.pyplot as plt
import numpy as np
from PIL import Image, ImageTk
import tkinter as tk




def ConvertToGrayScale(imageArray):
    grayScaleArray = 0.299*imageArray[:,:,0] + 0.587*imageArray[:,:,1] + 0.114*imageArray[:,:,2]
    return grayScaleArray.astype('uint8')

def Imshow2(imgArr1, imgArr2):
    plt.rcParams.update(plt.rcParamsDefault)
    f, (plot1, plot2) = plt.subplots(1, 2)
    plot1.imshow(imgArr1, cmap='gray', vmin=0, vmax=255)
    plot2.imshow(imgArr2, cmap='gray', vmin=0, vmax=255)
    plt.show()

def Imshow(imgArr1):
    plt.rcParams.update(plt.rcParamsDefault)
    f, (plot1) = plt.subplots(1, 1)
    plot1.imshow(imgArr1, cmap='gray', vmin=0, vmax=255)
    plt.show()

def PILImshow(imgArr1, title=None):
    imgArr1 = imgArr1.astype('uint8')
    imgObj = Image.fromarray(imgArr1)
    if title is not None:
        # window = tk.Tk()
        # window.title('Your Window Title')
        # tk_img = ImageTk.PhotoImage(imgObj)
        # label = tk.Label(window, image=tk_img)
        # label.pack()
        # window.mainloop()
        imgObj.show()

    else:
        imgObj.show()

    # Image.fromarray( imgArr2).show()
    # Image.fromarray( imgArr1 , 'L').save("C:\\Users\\ashis\\Documents\\Ashish\\EPR420\\Code\\Gray_Scale_Conversion\\Images\\imgArr1.png")
    # Image.fromarray( imgArr2 , 'L').save("C:\\Users\\ashis\\Documents\\Ashish\\EPR420\\Code\\Gray_Scale_Conversion\\Images\\imgArr2.png")


def BinImshow(imgArr1, flip):
    if(flip):
        imgArr1 = np.logical_not(imgArr1)
    imgArr1 = imgArr1*255
    imgArr1 = imgArr1.astype('uint8')
    f, (plot1) = plt.subplots(1, 1)
    plot1.imshow(imgArr1, cmap='gray', vmin=0, vmax=255)
    plt.show()



def BinPILImshow(imgArr1, flip):
    if (flip):
        imgArr1 = np.logical_not(imgArr1)
    imgArr1 = imgArr1*255
    imgArr1 = imgArr1.astype('uint8')
    Image.fromarray( imgArr1 , 'L').show()
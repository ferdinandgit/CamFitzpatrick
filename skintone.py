import cv2 
import numpy as np
import scipy
from scipy.interpolate import *
import keyboard
import csv

#=====Functions=====#

def keyboardInterrutp1(data):
    
    """Callback for keyboard event p is release.
    Args:
        data: keyboard.event not usefull here
    Return:
        - """

    global prelease
    prelease=True 


def flatten_list(matrix):
   
    """Transform 2d matrix in a list.
    Args:
        matrix: A array of array
    Return:
        A simple list"""

    flatlist = []
    for element in matrix:
        if type(element) is list:
            for item in element:
                flatlist.append(item)
        else:
            flatlist.append(element)
    return flatlist

def fitzPatrickClassification(ita):
    
    """classifier used to match ita with Fitzpatrick Scale.
    Args:
        ita: double where -90<=ita<=90
    Return:
        Fitzpatrick indice in range [|0;6|]"""

    if 37<ita:
         return 1
    elif -20<ita<=37:
         return 2
    elif -37.5<ita<=-20:
         return 3
    elif -55<ita<=-37.5:
        return 4
    elif -72.5<ita<=-55:
        return 5
    elif ita<=-72.5:
        return 6


def ita(lab):
    
    """ Ita calulation from Lab color space.
    Args: 
        lab:A array that contains [L,a,B] value.
    Return: 
        Ita Value."""

    return np.arctan((lab[0]-50)/lab[2])*180/np.pi

def bgrToRgb(rgb):
    return [rgb[2],rgb[1],rgb[0]]
    

def rgbToLab(inputColor):
    
    """Convert color from RGB colorspace to Lab colorsacpe
    Args:
        inputColor: A array that contains [R,G,B] int values (0<R,G,B<255).
    Returns:
        A array that contains [L,a,b] value."""

    num=0
    RGB=[0, 0, 0]
    for value in inputColor :
        value=float(value)/255
        if value>0.04045 :
           value=((value + 0.055)/1.055 )**2.4
        else :
           value=value/12.92
        RGB[num]=value * 100
        num=num + 1
    XYZ=[0, 0, 0,]

    X=RGB[0]*0.4124+RGB[1]*0.3576+RGB[2]*0.1805
    Y=RGB[0]*0.2126+RGB[1]*0.7152+RGB[2]*0.0722
    Z=RGB[0]*0.0193+RGB[1]*0.1192+RGB[2]*0.9505
   
    XYZ[0]=round(X,4)
    XYZ[1]=round(Y,4)
    XYZ[2]=round(Z,4)

    XYZ[0]=float(XYZ[0])/95.047    
    XYZ[1]=float(XYZ[1])/100.0          
    XYZ[2]=float(XYZ[2])/108.883       

    num=0
    for value in XYZ :
        if value>0.008856 :
            value=value**(0.3333333333333333)
        else:
            value=(7.787*value)+(16/116)

        XYZ[num]=value
        num=num+1

    Lab=[0,0,0]

    L=(116*XYZ[1])-16
    a=500*(XYZ[0]-XYZ[1])
    b=200*(XYZ[1]-XYZ[2])

    Lab[0]=round(L,4)
    Lab[1]=round(a,4)
    Lab[2]=round(b,4)

    return Lab



"""def estimateBrg(img):
    bleu = []
    red = []
    green = []
    wid,lgt,scale=np.shape(img)
    for i in range(wid):
        for j in range(lgt):
            if img[i][j][0]!=0 and img[i][j][1]!=0 and img[i][j][2]!=0:
                bleu.append(img[i][j][0])
                red.append(img[i][j][1])
                green.append(img[i][j][2])
    return [np.mean(bleu),np.mean(red),np.mean(green)]"""


def estimateBrg(img):
    
    """Estimation of the global color of an image.
    Args:
        img:a numpy.array with the following shape (x,y,3) where x,y are int.
    Return:
        a array with [bleu average value, green average value, red average value]"""

    bleu=np.average(img[:,:,:1])
    green=np.average(img[:,:,1:2])
    red=np.average(img[:,:,2:3])
    return [bleu,green,red]
    


def rescale(img,scalepercent):
    
    """Rescale image to scalepercent.
    Args:
        img: numpy.array withe the following shape (x,y,3) where x,y are int.
        scalepercent: scaling parameter 0<scalepercent.
    Returns:
        Resized image to scalepercent."""

    width = int(img.shape[1]*scalepercent/100)
    height = int(img.shape[0]*scalepercent/100)
    dim = (width, height)
    return cv2.resize(img, dim, interpolation = cv2.INTER_AREA)
  
def text(text,img,org):
    
    """Add text on img.
    Args:
        text: Displayed string.
        img: numpy.array with the following shape (x,y,3) where x,y are int.
        org: origin of top corner of the text area
    Returns:
        Image with text on desired origin."""
        
    font = cv2.FONT_HERSHEY_SIMPLEX
    fontScale = 2
    color = (255, 0, 0)
    thickness = 2
    return cv2.putText(img,text, org, font, fontScale, color, thickness, cv2.LINE_AA)

def bgrCorrection(fb,fg,fr,img):
    
    """Apply correction to each pixel image where Pixel_correct=f(Pixel_raw)*Prixel_raw.
    Args:
        fb: function that returns the correction factor for bleu pixel.
        fg: function that returns the correction factor for green pixel.
        fr: function that returns the correction factor for red pixel.
        img: numpy.array with the following shape (x,y,3) where x,y are int.
    Returns:
        Image with correction."""


    wid,lgt,size=np.shape(img)
    for i in range(wid):
        for k in range(lgt):
            img[i,k,0]*=fb(img[i,k,0])
            img[i,k,1]*=fg(img[i,k,1])
            img[i,k,2]*=fr(img[i,k,2])
    return img

#=====Main=====#

prelease=False #Flag used to activate an action in while loop when the key s is release
storecsv=[] # array for csv rows
gammared=[] #store correction factor for red image correction 
gammableu=[] #store correction factor for bleu image correction
gammagreen=[] #store correction factor for green image correction 
mesureredlist=[] #store red measure of each pixel from the camera
mesuregreenlist=[] #store green measure of each pixel from the camera
mesurebleulist=[] #store bleu measure of each pixel from the camera

#red the csv file with references and measures from the camera. Calibration csv is composed of 6 rows, 3 for RGB reference, 3 for RGB measure.  
with open('calibration.csv', newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        storecsv.append([row['R_ref'],row['G_ref'],row['B_ref'], row['R'],row['G'],row['B']])

#Remove the column descriptor of the csv file.
storecsv.pop(1)

#Store value for interpolation calculation 
for couple in storecsv:
    gammared.append(float(couple[0])/float(couple[3]))
    gammagreen.append(float(couple[1])/float(couple[4]))
    gammableu.append(float(couple[2])/float(couple[5]))
    mesureredlist.append(float(couple[3]))
    mesuregreenlist.append(float(couple[4]))
    mesurebleulist.append(float(couple[5]))

#determine R,G,B correction functions 
fbleu=scipy.interpolate.interp1d(mesurebleulist,gammableu,bounds_error=False,fill_value="extrapolate")
fgreen=scipy.interpolate.interp1d(mesuregreenlist,gammagreen,bounds_error=False,fill_value="extrapolate")
fred=scipy.interpolate.interp1d(mesureredlist,gammared,bounds_error=False,fill_value="extrapolate")

#Open video flow of the microscope  
#!!!!!WARNING vid = cv2.VideoCapture(x), x should be changed if your run the script on a orther computer WARNING!!!!!!
vid = cv2.VideoCapture(2)

#Setup keyboardInterrupt call keyboardInterrutp1 when p is release
keyboard.on_release_key('p',keyboardInterrutp1)


indice=0 #displayed Fitzpatrick indice 
itavalue=0 #displayed ita value 
lab=[0 for k in range(3)] #displayed lab value

while(True):
      
    # Capture the video frame
    # by frame
    ret, frame = vid.read()
    try:
        a,b,c=np.shape(frame) #this will fail if there is no video input 
    except:
        print("Check your video input")
        break

    #Draw a rectangle on the frame 
    cv2.rectangle(frame, (int(b/2)-100,int(a/2)-100), (int(b/2)+100,int(a/2)+100), (0, 255, 0), 3)
    
    #Crop the area in the green triangle
    cropped_frame = frame[(int(a/2)-90):(int(a/2)+90),(int(b/2)-90):(int(b/2)+90)]
    
    #Estimation of the color in the green triangle 
    brg=estimateBrg(cropped_frame)
    
    #Write data on the left corner of the screen
    frame=text("Phototype"+str(indice)+"_"+str(itavalue),frame,(50,50))
    frame=text("l:"+str(lab[0])+"a:"+str(lab[1])+"b:"+str(lab[2]),frame,(50,150))
   
    
    if prelease: #when p is release
        
        #Apply  color correction to the cropped_frame
        cropped_frame = bgrCorrection(fbleu,fgreen,fred,cropped_frame)
        lab=rgbToLab(bgrToRgb(brg))
        if lab[2]<=0:
            lab[2]=0.0000001
        itavalue=ita(lab)
        indice=fitzPatrickClassification(itavalue)
        cv2.imshow('Corrected_IMG',cropped_frame)
        cv2.waitKey(1)
        prelease=False
    

    cv2.imshow('Skintone.py', frame)
      
    # the 'q' button is set as the
    # quitting button you may use any
    # desired button of your choice
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
  
# After the loop release the cap object
vid.release()
# Destroy all the windows
cv2.destroyAllWindows()



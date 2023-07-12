import cv2 
import numpy as np
import scipy
from scipy.interpolate import *
import keyboard

#=====Functions=====#

def keyboardInterrutp1(data):
    
    """Callback for keyboard event s is release.
    Args:
        data: keyboard.event not usefull here
    Return:
        - """

    global frelease
    frelease=True 

def keyboardInterrupt(data):
    
    """Callback for keyboard event s is release.
    Args:
        data: keyboard.event not usefull here
    Return:
        - """
    
    global srelease
    srelease = True


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

    if 0<ita:
         return 1
    elif -37<ita<=0:
         return 2
    elif -60<ita<=-37:
         return 3
    elif -70<ita<=-60:
        return 4
    elif -80<ita<=-70:
        return 5
    elif ita<=-80:
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

mesure=[0 for k in range(4)]
reference=[]
gammalist=[]
#bgrref=[[180,187,231],[156,171,218],[127,144,194],[98,116,160],[87,105,147],[114,113,129],[255,255,255],[0,0,0]]
bgrref = [[43,229,255],[119,63,213],[219,151,0],[71,74,78]]
flag=[1 for k in range(4)]
vid = cv2.VideoCapture(2)
srelease=False
frelease=False
mesure=[[0,0,0] for k in range(4)]
i=0 
avggammableu=0
avggammared=0
avggammagreen=0


keyboard.on_release_key('s',keyboardInterrupt,False)
while(True):
      
    ret, frame = vid.read()
    a,b,c=np.shape(frame)
    cv2.rectangle(frame, (int(b/2)-100,int(a/2)-100), (int(b/2)+100,int(a/2)+100), (0, 255, 0), 3)
    cropped_frame = frame[(int(a/2)-90):(int(a/2)+90),(int(b/2)-90):(int(b/2)+90)]
    
    bleu=np.average(cropped_frame[:,:,:1])
    green=np.average(cropped_frame[:,:,1:2])
    red=np.average(cropped_frame[:,:,2:3])
    

    frame=text(str(i),frame,(50,50))  
    frame=text("RGB: "+str(round(red))+','+str(round(green))+','+str(round(bleu)),frame,(50,150))
    
    cv2.imshow('frame', frame)
      
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    
        
    if srelease:
        if i<4:
            i+=1
            if bgrref[i-1][0]!=bleu:
                gammableu=bgrref[i-1][0]/bleu
            else: 
                gammableu=1
            if bgrref[i-1][1]!=green:
                gammagreen=bgrref[i-1][1]/green
            else:
                gammagreen=1
            if bgrref[i-1][2]!=red:
                gammared=bgrref[i-1][2]/red
            else:
                gammared=1
            gammalist.append([gammableu,gammagreen,gammared])
            mesure[i-1][0]=bleu
            mesure[i-1][1]=green
            mesure[i-1][2]=red
            print(gammalist)
        srelease=False 





gammalist=np.array(gammalist)
mesure=np.array(mesure)

gammableulist=flatten_list(gammalist[:,:1].tolist())
gammagreenlist=flatten_list(gammalist[:,1:2].tolist())
gammaredlist=flatten_list(gammalist[:,2:3].tolist())

mesurebleulist=flatten_list(mesure[:,:1].tolist())
mesuregreenlist=flatten_list(mesure[:,1:2].tolist())
mesureredlist=flatten_list(mesure[:,2:3].tolist())

fbleu=scipy.interpolate.interp1d(mesurebleulist,gammableulist,bounds_error=False,fill_value="extrapolate")
fgreen=scipy.interpolate.interp1d(mesuregreenlist,gammagreenlist,bounds_error=False,fill_value="extrapolate")
fred=scipy.interpolate.interp1d(mesureredlist,gammaredlist,bounds_error=False,fill_value="extrapolate")

vid.release()
cv2.destroyAllWindows()

    

vid = cv2.VideoCapture(2)

keyboard.on_release_key('p',keyboardInterrutp1)
indice=0
itavalue=0
lab=[0 for k in range(3)]
while(True):
      
    # Capture the video frame
    # by frame
    ret, frame = vid.read()
    a,b,c=np.shape(frame)
    cv2.rectangle(frame, (int(b/2)-100,int(a/2)-100), (int(b/2)+100,int(a/2)+100), (0, 255, 0), 3)
    cropped_frame = frame[(int(a/2)-90):(int(a/2)+90),(int(b/2)-90):(int(b/2)+90)]
    #cropped_frame = bgrGammaCorrection(fbleu,fgreen,fred,cropped_frame)
    brg=estimateBrg(cropped_frame)
        
    frame=text("Phototype"+str(indice)+"_"+str(itavalue),frame,(50,50))
    frame=text("l:"+str(lab[0])+"a:"+str(lab[1])+"b:"+str(lab[2]),frame,(50,150))
    
    if frelease:
        cropped_frame = bgrCorrection(fbleu,fgreen,fred,cropped_frame)
        lab=rgbToLab(bgrToRgb(brg))
        if lab[2]<=0:
            lab[2]=0.0000001
        itavalue=ita(lab)
        indice=fitzPatrickClassification(itavalue)
        cv2.imshow('cropped_frame',cropped_frame)
        cv2.waitKey(1)
        frelease=False

    cv2.imshow('frame', frame)
      
    # the 'q' button is set as the
    # quitting button you may use any
    # desired button of your choice
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
  
# After the loop release the cap object
vid.release()
# Destroy all the windows
cv2.destroyAllWindows()



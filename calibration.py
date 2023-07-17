import cv2 
import numpy as np
import scipy
from scipy.interpolate import *
import keyboard
import csv
from tkinter import *
from tkinter.simpledialog import askstring
from tkinter.messagebox import showinfo

#======Functions=====#

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


def keyboardInterrupt(data):
    
    """Callback for keyboard event s is release.
    Args:
        data: keyboard.event not usefull here
    Return:
        - """
    
    global srelease
    srelease = True

def askUser():

    """ Popup text box asking for RGB code
    Args:
        -
    Return 
        Array with rgb code """

    a=''
    RGBref=[]
    name = askstring('RBG reference', 'R,G,B?')
    for i in name:
        if i!= ',':
            a+=i
        else:
            print(a)
            RGBref.append(a)
            a=''
    RGBref.append(a)
    return RGBref



#======Main======#

srelease=False #Flag used to activate the action in while loop when the key s is release
nbscannedcolor=0 #count the number of scanned color 
row=[] #store data that will be writed in the csv file  
references=[] #store reference color code.
nbsamples=110 #


#Open video flow of the microscope  
#!!!!!WARNING vid = cv2.VideoCapture(x), x should be changed if your run the script on a orther computer WARNING!!!!!!

vid = cv2.VideoCapture(2)

#Setup keyboard interruption with keyboardInterrupt callback 

keyboard.on_release_key('s',keyboardInterrupt,False)

while(True):
          
    ret, frame = vid.read()
    a,b,c=np.shape(frame)

    #Draw a rectangle on the frame
    cv2.rectangle(frame, (int(b/2)-100,int(a/2)-100), (int(b/2)+100,int(a/2)+100), (0, 255, 0), 3)
    
    #Crop the area in the green triangle 
    cropped_frame = frame[(int(a/2)-90):(int(a/2)+90),(int(b/2)-90):(int(b/2)+90)]
    

    #BGR average of the cropped_frame
    bleu=np.average(cropped_frame[:,:,:1])
    green=np.average(cropped_frame[:,:,1:2])
    red=np.average(cropped_frame[:,:,2:3])

    #Print usefull text on the frame 
    frame=text(str(nbscannedcolor),frame,(50,50))  
    frame=text("RGB: "+str(round(red))+','+str(round(green))+','+str(round(bleu)),frame,(50,150))
    
    #display in the frame 
    cv2.imshow('frame', frame)
     
    #if the the key q is pressed wh
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    
    #when s key is release => store mesured data and reference color code in row for csv writing      
    if srelease:
        colorref=askUser()
        if nbscannedcolor<nbsamples:
            row.append([colorref[0],colorref[1],colorref[2],red,green,bleu,nbscannedcolor])
            nbscannedcolor+=1
            srelease=False
        else: 
            print(max)

#close video flow and close windosw
vid.release()
cv2.destroyAllWindows()

#set each fileds of thre csv file

fields=["R_ref","G_ref","B_ref","R","G","B"]

#write row to csv following fiels parameters orders

with open('calibration.csv', 'w') as f:
     
    write = csv.writer(f)
    write.writerow(fields)
    write.writerows(row)



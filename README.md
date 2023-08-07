# CamFitzpatrick 
--------------------------------
This project determine your phototype with the help of a macro camera.

## Features
- Camera Calibration with references colors samples.
- Phototye estimation with Fitzpatrick Scale.

## Tech
CameFitzpatrick uses a number python open source projects to work properly:

- [OpenCV] - Python library used for computer vision.
- [csv] - Python csv editor.
- [numpy] - Python math extension.
- [scipy] - SciPy provides algorithms for o{:.centered}.
- [keyboard] - Hook global events, register hotkeys, simulate key presses and much more.



## Installation

This project requires [Python](https://www.python.org/) v3.11.0+ to run.

Start python virtual environement installation script   
for linux users:
```sh
./linuxvenv.sh
```

for windows users: 
```sh
.\winvenv.bat 
```

## Camera Calibration
In order to calibrate your camera you need this kind of color samples. You can use other colors samples as long as they are not printed otherwise the calibration will not be efficient. Painted samples will be preferred.


![Pantone SkinTone Guide](https://www.pantone.com/media/catalog/product/s/t/stg202-pantone-skintone-guide-product-1.jpg?quality=95&fit=bounds&height=400&width=1200&canvas=1200:1200)
 ![Pantone The Plus Series](https://www.pantone.com/media/catalog/product/g/p/gp1601b-pantone-pms-formula-guide-coated-uncoated-product-1.jpg?quality=95&height=400&width=400&canvas=307:307)

Before running any code make shure that your video input is the rigth one in each python script.
```python
videoinput=2 #find the number that is associated with your video device 
srelease=False
nbscannedcolors=0
```
Then in order to start calibration run
for linux users:
```sh
sudo startcalibration.sh 
```
for windows users:
```sh
startcalibration.bat
```

There is 2 keys to control the script:
 - S key is used to estimate and save the avrage color in the green rectangle.
 - Q key is used to kill the script. 

In order to start measurement, adjust your camera position to make the square above the reference color and press S to save the color and enter the RGB value of your reference in the text box. .

The script is outpouting a csv file with 6 rows, 3 rows for the RGB refenrence color value, 3 rows for the RGB mesured color value. 

Thus we can determine 3 simples functions that give the correction factor for each RGB pixel components knowing the mesured RGB value of the pixel. Let's consider ![equation](https://latex.codecogs.com/svg.image?\gamma) the corrective factor, each functions is declared like:

![equation](https://latex.codecogs.com/svg.image?\gamma=f_{color}(Color_{mesured})=\frac{Color_{reference}}{Color_{mesured}})

With all collected samples we can determine the ![equation](https://latex.codecogs.com/svg.image?\gamma) for each pixel using a scipy first degree interpolation  

 ![equation](https://latex.codecogs.com/svg.image?fbleu(B_{mesured})*B_{mesured}=B_{corrected}) 
 ![equation](https://latex.codecogs.com/svg.image?fgreen(G_{mesured})*G_{mesured}=G_{corrected}) 
 ![equation](https://latex.codecogs.com/svg.image?fred(R_{mesured})*R_{mesured}=R_{corrected}) 
 
## Skin Tone determination

Make shure that the calibration csv file path is the good one in the python script

```python
with open('calibration.csv', newline='') as csvfile: #Change your file path here 
    reader = csv.DictReader(csvfile)
    for row in reader:
```

In order to start skin Tone determination run:

for linux users: 
```sh
sudo startskintone.py 
```
for windows users:
```sh
startskintone.bat
```

There is 2 keys to control the script:
 - P key is used to estimate the skin tone.
 - Q key is used to kill the script. 

Adjust your camera position to make the square above the skin. Once P is pressed a second windows open and display the corrected image and the skin tone estimation is displayed in the left top corner of the main window.

## Appendix 


I used this [Camera](https://www.amazon.fr/Bysameyee-Microscope-3840x2160P-dinspection-grossissement/dp/B09NBY6G9S?source=ps-sl-shoppingads-lpcontext&ref_=fplfs&psc=1&smid=A1JXU0GT57OBZF) to test each of my scripts, few camera brackets 3D files are also avaliable on the repo. 
































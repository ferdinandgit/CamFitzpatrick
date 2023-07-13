# CamFitzpatrick 
--------------------------------
This project determine your phototype with the help of a macro camera.

## Features
- Camera Calibration with Pantone SkinTone Guide.
- Phototye estimation with Fitzpatrick Scale.

## Tech
CameFitzpatrick uses a number python open source projects to work properly:

- [OpenCV] - Python library used for computer vision.
- [csv] - Python csv editor.
- [numpy] - Python math extension.
- [scipy] - SciPy provides algorithms for o{:.centered}.
- [keyboard] - Hook global events, register hotkeys, simulate key presses and much more.



## Installation

This project requires [Python](https://www.python.org/) v3.10.0+ to run.

Install all the dependencies 

```sh
pip3 install requirements.txt 
```
OpenCV can be installed:
- with apt for linux users
```sh
sudo apt-get install python3-opencv
```
- follow this tutorial for windows user : [Windows Install](https://docs.opencv.org/4.x/d5/de5/tutorial_py_setup_in_windows.html)

## Camera Calibration
In order to calibrate your camera you need such color samples. Youc can use other colors samples as long as the are not printed otherwise the calibratiosn will not be effective. Paint samples will be preferred.


![Pantone SkinTone Guide](https://www.pantone.com/media/catalog/product/s/t/stg202-pantone-skintone-guide-product-1.jpg?quality=95&fit=bounds&height=400&width=1200&canvas=1200:1200)
 ![Pantone The Plus Series](https://www.pantone.com/media/catalog/product/g/p/gp1601b-pantone-pms-formula-guide-coated-uncoated-product-1.jpg?quality=95&height=400&width=400&canvas=307:307)

Before running any code make shure that your video input is the rigth one in each python script.
```python
videoinput=2 #find the number that is associated with your video device 
srelease=False
nbscannedcolors=0
```
Then enter the number of samples that will be use for calibration 
```python 
nbsamples=110 #in our case the Pantone SkinTone Guide is made of 110 tones 
 ```
Then in order to start calibration enter in your shell 

```sh
sudo python3 calibration.py 
```
These windows will appear on your screen. 

There is 2 keys to control the script:
 - S key is used to estimate and save the avrage color in the green rectangle.
 - Q key is used to kill the script. 

In order to start mesurement enter the RGB value of your reference in the text box. Adjust your camera posiitin to make the square above the reference color and press S to save the color. When you have reach the end of your sampling end will appear on the top left corner of the screen.

The script is outpouting a csv file with 6 rows, 3 rows for the RGB refenrence color value, 3 rows for the RGB mesured color value. 

Thus we can determine 3 simples functions that give the corrective factor for each RGB pixel components knowing the mesured RGB value of the pixel. 


































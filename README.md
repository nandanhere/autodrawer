# Autodrawer

Autodrawer is an automatic paint/skribbl.io drawing application with the intent of being as user friendly as possible.
![example](https://github.com/nandanhere/autodrawer/blob/main/readme/walle.png)


## Installation

- After cloning the repo, make sure you install google_image_download , tkinter and pyautogui ,beepy and pynput by running the    following:  
    `pip install google_images_download`  
    `pip install pyautogui`
    `pip install tk`  
    `pip install pynput`
    `pip install beepy`  

# Usage:
Note that Autodrawer works only on drawing applications with a horizontal color palette. 
- The first dialog box allows you to configure what to draw.  *The default is a Picture of Donald duck, in case of any errors.* 
  - -  You can also select the number of colors in the color palette and also the resolution of the image to be drawn (higher will take more time)   <br>
   ![first dialog box](https://github.com/nandanhere/autodrawer/blob/main/readme/dialog1.png) 

 - The second dialog box is a confirmation box in case you would like to cancel the drawing. (Autodrawer cannot be stopped when it is drawing.)    <br>
		![confirmation dialog](https://github.com/nandanhere/autodrawer/blob/main/readme/dialog2.png)
   --On confirming, click on the first color in the color palette from the **top left**. An audio cue will play to  indicate the click has been recorded.  
 - Next, click on the paint area. this point will be the reference point from which the Drawer will start.   <br>
	 ![outcome](https://github.com/nandanhere/autodrawer/blob/main/readme/horse.png)
			
## Note

This program doesn't intend to use copyrighted materials/images from google. You can use your own images by adding the image as sample.jpeg in the directory of Autodrawer , and keeping default settings while drawing.

### Credits/Resources:
[@theNova22 for his amazing idea and implementation of the idea](https://github.com/TheNova22/Skribbot)
[Tom Schimansky  for tkinter custom button](https://github.com/TomSchimansky/GuitarTuner/blob/master/documentation/tkinter_custom_button.py)

# Autodrawer - inspired by https://github.com/TheNova22/skribbot, with some GUI added
# tkintercustombutton from https://github.com/TomSchimansky/GuitarTuner/blob/master/documentation/tkinter_custom_button.py
import sys,os,beepy,numpy,shutil
import tkinter as tk
from tkinter_custom_button import TkinterCustomButton 
import pyautogui as pg
from pynput import mouse,keyboard
from PIL import Image
from google_images_download import google_images_download
pg.PAUSE = 0 # change to appropriate seconds for speeed. we keep it 0 for fast drawing
# Top level window
imageLoc = ""
# ----------Portion of code that gets the input---------------START
firstWindow = tk.Tk()
firstWindow.title("Autodrawer")
firstWindow.geometry("600x150")
l1 = tk.Label(firstWindow, text="Enter the thing to be drawn (default is donald duck)", padx=5); l1.grid(row = 0)
l2 = tk.Label(firstWindow, text="how many colors are there in a row?(default is 11 for skribbl)", padx=5);l2.grid(row=2)
l3 = tk.Label(firstWindow, text="how big do you want it? (default is 200x200)", padx=5);l3.grid(row=4)
# following will keep donald duck as default. if clicked on it it will allow to change it,ie it clears the input
firstclick = True
def exitprogram():
    if len(imageLoc) != 0:
            os.remove(imageLoc)
    sys.exit()
def on_entry_click(event):
    # function that gets called whenever imageWord entry is clicked        
    global firstclick
    if firstclick: # if this is the first time they clicked it
        firstclick = False
        imageWord.delete(0, "end") # delete all the text in the entry
imageWord = tk.Entry(firstWindow) ; imageWord.insert(0,'Donald Duck') ; imageWord.bind('<FocusIn>', on_entry_click)
options1 = list(range(1,20)); options2 = [100,200,300] 
variable1 = tk.StringVar(firstWindow); variable2 = tk.StringVar(firstWindow)
variable1.set(options1[10]) ;variable2.set(options2[1])
colorsOptions = tk.OptionMenu(firstWindow, variable1,*options1)
sizeOptions = tk.OptionMenu(firstWindow, variable2,*options2)
imageWord.grid(row=1); colorsOptions.grid(row = 3); sizeOptions.grid(row = 5)
word = 'Donald duck' # what Autodrawer will draw
nosOfColors = options1[10] # whether it is in paint or in skribbl
dimension = options2[1] # either 100x100, 200x200,300x300
firstWindow.protocol("WM_DELETE_WINDOW",exitprogram)

def updateInput():
    global word, nosOfColors, dimension
    word = imageWord.get()
    nosOfColors = int(variable1.get())
    dimension = int(variable2.get())
    for w in [imageWord,colorsOptions,sizeOptions,l1,l2,l3]:
        w.destroy()
    button_1.place(relx=-100, rely=-100, anchor=tk.CENTER) 
    getImage()
    updateWindow()
button_1 = TkinterCustomButton(text="Click to start!", corner_radius=10, command=updateInput)
button_1.place(relx=0.85, rely=0.5, anchor=tk.CENTER)  

# Label Creation
# ----------Portion of code that gets the input---------------END

# ----------Portion of code that downloads the image and saves it in PWD---------------START
def getImage():
    global imageLoc
    response = google_images_download.googleimagesdownload()
    arguments = {"keywords": word, "limit":1, "print_urls":True, 'safe_search':True, 'exact_size':'{},{}'.format(dimension,dimension), 'type': 'clipart', 'format': 'jpg','no_directory' : True}
    imageLoc = ""
    try:
        if 'Donald Duck' in word: raise Exception()
        paths = response.download(arguments)
        imageLoc = paths[0][word][0]
    except:
        imageLoc = sys.path[0] + '/sample.jpeg'
        shutil.copyfile(imageLoc,sys.path[0] + '/image.jpeg')
        imageLoc = sys.path[0] + '/image.jpeg'
# ----------Portion of code that downloads the image and saves it in PWD---------------END

# ----------Final dialog window to start the drawing---------------START
clickCount = -1
def proceed(choice):
    if choice:
        firstWindow.destroy()
        global clickCount
        clickCount += 1
def updateWindow(): 
    firstWindow.geometry("600x50")
    firstWindow.title("Autodrawer")
    a = tk.Label(firstWindow, text="Click on the location of the first color from the top left, then the location to start drawing from", padx=5).grid(row = 0)
    b = tk.Button(text="Ok",command=lambda: proceed(True)).grid(row=1,column=0)
    c = tk.Button(text="Cancel",command=exitprogram)
    c.grid(row=1,column=1)
    c.place(relx=0.6,rely=0.45)
firstWindow.protocol("WM_DELETE_WINDOW",exitprogram)
firstWindow.mainloop()
# ----------Final dialog window to start the drawing---------------END

# ----------Portion of code that captures the clicks---------------START
(w_x,w_y) = (0,0)
(s_x,s_y) = (0,0)
def getTheClicks(x, y, button, pressed):
    global listener
    global clickCount
    global w_x,w_y,s_x,s_y
    if pressed:
        beepy.beep(sound=1)
        if clickCount == 0:
            (w_x,w_y) = (x,y)
        clickCount += 1
        if clickCount == 2:
            (s_x,s_y) = (x,y)
            listener.stop()
# sf = lambda x,y,z,e:print("{},{}".format(x,y))
listener = mouse.Listener(on_click=getTheClicks)
# Click 1 : get the location of the first color from the top left.
# Click 2 : get the location of the start point to draw
listener.start()
while(clickCount != 2):
    print("",end="")
# ----------Portion of code that captures the clicks---------------END

# ----------Recording all the colors in the palette of paint/skribbl---------------START
im = pg.screenshot('tempAutodrawer.png')
colortable = []
colorvalues = []
for i in range(nosOfColors):
    colortable.append((int(w_x + 25 * i),int(w_y)))
    colorvalues.append(im.getpixel(colortable[-1])[:-1]) #type: ignore
for i in range(nosOfColors):
    colortable.append((int(w_x + 25 * i),int(w_y + 30)))
    pixel = im.getpixel(colortable[-1])                 #type: ignore
    colorvalues.append(pixel[:-1] if len(pixel) > 3  else pixel) #type: ignore
pal = []
for pixel in colorvalues:
    pal += list(pixel)
pal += [0 for _ in range(768 - len(pal))]
# ----------Recording all the colors in the palette of paint/skribbl---------------STOP

# ----------Image processing bit---------------START
def rh(r,g,b):
    return "#{:02x}{:02x}{:02x}".format(r,g,b)
def alpha_to_color(image, color=(255, 255, 255)):
    # Source: http://stackoverflow.com/a/9166671/284318
    x = numpy.array(image)
    r, g, b, a = numpy.rollaxis(x, axis=-1)
    r[a == 0] = color[0]
    g[a == 0] = color[1]
    b[a == 0] = color[2] 
    x = numpy.dstack([r, g, b, a])
    return Image.fromarray(x, 'RGBA')
img = Image.open(imageLoc)
copy = Image.open(imageLoc)
img = img.resize((dimension,dimension))
palette = Image.new("P",(16,16))
palette.putpalette(pal)
img = img.convert("RGB").quantize(palette=palette)
img = img.convert("RGB")

img.save(imageLoc)
# ----------Image processing bit---------------STOP

# ----------Converting the image into a matrix of pixel values---------------START
mat = numpy.asarray(img)
colordict = dict()
def roundColor(r,g,b):
    global colortable,colorvalues
    index = 0
    max = 9999
    diff = 0
    for i in range(len(colorvalues)):
        (a,bb,c) = colorvalues[i]
        diff = abs(r - a) + abs(g - bb) + abs (b - c)
        if abs(diff) < max:
            index = i
            max = abs(diff)
    if max > 10:
        return 0
    return index
mmat = [[(0,0,0) for _ in range(len(mat[0]))] for _ in range(len(mat))]
for i in range(0,len(mat),1):
    for j in range(0,len(mat[1]),1):
        (r,g,b) = mat[i][j]
        hex = rh(r,g,b)
        if hex not in colordict.keys():
            colordict[hex] = colorvalues[roundColor(r,g,b)]
        mmat[i][j] = colordict[hex]
# ----------Converting the image into a matrix of pixel values---------------STOP

# ----------Loop where painting will happen---------------START
# TODO make a way for the user to exit the loop with a keypress
for i in range(len(colortable)):
    if i == 1:
        # print(colorvalues[i])
        continue
    pg.click(colortable[i])
    (a,b,c) = colorvalues[i]
    if a == b == c == 255 : continue
    for y in range(0,len(mat),5 if dimension == 300 else 3):
        for x in range(0,len(mat[0]),5 if dimension == 300 else 3):
            (r,g,bb) = mmat[y][x]
            if r == a and g == b and c == bb:
                pg.click(s_x + x, s_y + y)
# ----------Loop where painting will happen---------------STOP
# finishing code
beepy.beep(5)
if "/sample.jpeg" not in imageLoc:
    os.remove(imageLoc)
os.remove('tempAutodrawer.png')
 


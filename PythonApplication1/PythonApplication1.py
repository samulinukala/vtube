from audioop import rms
import audioop
from math import factorial
from tkinter import *
from tkinter.tix import IMAGE
from PIL import Image, ImageTk
from pyaudio import *
import pyaudio

root = Tk()
root.geometry("498x411")

# Load the image and resize it to fit the window

image = Image.open("1.png")
image = image.resize((root.winfo_width(), root.winfo_height()))
photo = ImageTk.PhotoImage(image)
image2 = Image.open("2.png")
image2 = image2.resize((root.winfo_width(), root.winfo_height()))
photo2 = ImageTk.PhotoImage(image2)
leftimg=image
rightimg=image2
limitvoice= 30
limitquiet=20
fade_duration = 30 
fade_val=0
quiet=True
momentum=0
momentumAmmount=7
momentumValue=2
blend=photo


# Create a label to display the image
label = Label(root, image=photo)
def fadepic(img1,img2,fadeval) :
    # Create a new image with the same size
   # number of steps for the fade
    img1=img1.convert("RGBA")
    img2=img2.convert("RGBA")
   
    global fade_duration
    if fadeval>fade_duration:
        fadeval=fade_duration
    elif fadeval<0:
        fade_val=0
    alpha = int(255 *  ((fade_duration-fadeval)/fade_duration))
    img2_with_alpha = img2.copy()
    img2_with_alpha.putalpha(alpha)
    
    
    blended = Image.alpha_composite(img1, img2_with_alpha)

    return ImageTk.PhotoImage( blended)
p=pyaudio.PyAudio()
stream = p.open(format=pyaudio.paInt16,
                channels=1,
                rate=44100,
                input=True,
                frames_per_buffer=1024)
def checkAudio():
 
      
       
       
        global momentum

        global fade_duration
        global fade_val
        global blend
        image = Image.open("1.png")
        image = image.resize((root.winfo_width(), root.winfo_height()))
        image2 = Image.open("2.png")
        image2 = image2.resize((root.winfo_width(), root.winfo_height()))
        data=stream.read(1024)
        rms=audioop.rms(data,2)
        leftimg=image
        rightimg=image2
        max_n=100
        n=min(int(rms//2),max_n)
        blank=n;
       
        if blank>limitquiet : 
            quiet=False
        else :
            quiet=True

        if fade_val>fade_duration:
            fade_val=fade_duration
        elif fade_val<0:
            fade_val=0
        if momentum>0:
            fade_val=fade_val+momentumValue
            momentum=momentum-1
       
        if blank>limitvoice :
            fade_val= fade_val+2
            momentum= momentumAmmount
        elif quiet :
               
            fade_val=fade_val-2
                   
               
   
            

        blend=fadepic(leftimg,rightimg,fade_val)
        label.configure(image=blend)
        label.image=blend
        print("volume level: ", blank)
        print("fadeval: ", fade_val)
        print("quiet: ",quiet)
        print("")
        print("")
        print("")
        print("")
       
        root.after(5,checkAudio)
       

          
    
            
      
label.pack(fill=BOTH, expand=YES)
# Function to resize the image when the window is resized
def resize_image(event):
    global photo
    
    # Resize the image to fit the new window size
    image = Image.open("1.png")
    image = image.resize((event.width, event.height))
    photo = ImageTk.PhotoImage(image)
    
    # Update the image on the label
    label.configure(image=photo)
    label.image = photo

# Bind the resize_image function to the <Configure> event
root.bind("<Configure>", resize_image)
root.after(50,checkAudio)


root.mainloop()


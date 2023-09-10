import pygame,sys
from pygame.locals import *
import numpy as np
from keras.models import load_model
import cv2

WINDOWSIZEX,WINDOWSIZEY=640,480

BOUNDRYINC=5
WHITE=(255,255,255)
BLACK=(0,0,0)
RED=(255,0,0)

IMAGESAVE=False
PREDICT=False

MODEL=load_model("bestModel.h5")

LABELS={
    0:"Zero",
    1:"One",
    2:"Two",
    3:"Three",
    4:"Four",
    5:"Five",
    6:"Six",
    7:"Seven",
    8:"Eight",
    9:"Nine"
}

# initialize pygame
pygame.init()

# FONT=pygame.font.Font("freesansbold.tff",18)
FONT= pygame.font.Font('freesansbold.ttf', 32)

DISPLAYSURFACE=pygame.display.set_mode((WINDOWSIZEX,WINDOWSIZEY))
pygame.display.set_caption("Digit Board")

iswriting=False

number_xcord=[]
number_ycord=[]
image_cnt=1

while True:
    for event in pygame.event.get():
        if event.type==QUIT :
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
           
            # if keydown event happened
            # than printing a string to output
            print("A key has been pressed")  
        if event.type==MOUSEMOTION and iswriting:
            xcord,ycord=event.pos
            pygame.draw.circle(DISPLAYSURFACE,WHITE,(xcord,ycord),4, 0)
            number_xcord.append(xcord)
            number_ycord.append(ycord)

        if event.type==MOUSEBUTTONDOWN :
            iswriting=True

        if event.type==MOUSEBUTTONUP :
            iswriting=False
            number_xcord=sorted(number_xcord)
            number_ycord=sorted(number_ycord)

            try:                    
                    rect_min_x,rect_max_x=max(number_xcord[0]-BOUNDRYINC,0),min(WINDOWSIZEX,number_xcord[-1]+BOUNDRYINC)
                    rect_min_y,rect_max_y=max(number_ycord[0]-BOUNDRYINC,0),min(WINDOWSIZEY,number_ycord[-1]+BOUNDRYINC)
            except:
                    continue


            number_xcord=[]
            number_ycord=[]

            img_arr=np.array(pygame.PixelArray(DISPLAYSURFACE))[rect_min_x:rect_max_x, rect_min_y:rect_max_y].T.astype(np.float32)
            PREDICT=True

            if IMAGESAVE:
                cv2.imwrite("image.png")
                image_cnt+=1

            if PREDICT :
                image=cv2.resize(img_arr,(28,28))
                image=np.pad(image,(10,10),'constant',constant_values=0)
                image=cv2.resize(image,(28,28))/255

                try:                    
                    label=str(LABELS[np.argmax(MODEL.predict(image.reshape(1,28,28,1)))])
                except:
                    continue

                textSurface=FONT.render(label,True,RED,WHITE)
                textRecObj=textSurface.get_rect()
                textRecObj.left,textRecObj.bottom= rect_min_x,rect_max_y

                DISPLAYSURFACE.blit(textSurface,textRecObj)

        if event.type==KEYDOWN :
            if event.unicode== "K_DELETE" or "n" :
                DISPLAYSURFACE.fill(BLACK)
            if event.unicode== "K_KP_ENTER" :  
                IMAGESAVE=True
                cv2.imwrite("image2.png")
            if event.unicode== "K_ESCAPE":
                 print("ESCAPE PRESSED")
                 pygame.quit()
                 sys.exit()
    
        pygame.display.update()
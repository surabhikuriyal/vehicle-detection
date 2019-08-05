# -*- coding: utf-8 -*-

import cv2
import numpy as np
import os
import math
import random
import time
import pandas as pd
import datetime
import smtplib
import Main

cascade_src = 'cars.xml'
video_src = 'carsmobile4.mp4'
#print(cascade_src)
cap = cv2.VideoCapture(video_src)

car_cascade = cv2.CascadeClassifier(cascade_src)
print(cascade_src)
TIME=[]
VEL=[]
i=0
wide=0.1   #depends upon size of car(~2.5)
flag=True

start=end=0
time_diff=0
ret, img = cap.read()

while ret:
    #img=cv2.rotate(img, cv2.ROTATE_90_CLOCKWISE)
    try:
        height,width,chan=img.shape
    except AttributeError:
        print(ret)
        break
    if img.shape[0]>480:
        scale_percent = 50 
        width = int(img.shape[1] * scale_percent / 100) 
        height = int(img.shape[0] * scale_percent / 100) 
        dim = (width, height) 
        img = cv2.resize(img, dim, interpolation = cv2.INTER_AREA)
    i=i+1
    if (type(img) == type(None)):
        break
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    clone=img.copy()
    cars = car_cascade.detectMultiScale(gray, 1.1, 2)

    for (x,y,w,h) in cars:
        cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,255),2)
        crop_img=clone[y:y+h,x:x+w]
        center_x=(2*x+w)/2
        center_y=(2*y+h)/2
        #print(center_x,center_y)
        dist1=((wide*668.748634441)/w)
        #print("Distance from car:",round(dist1,2),"m")
        roi_gray = gray[y:y+h,x:x+w]
        roi_color = img[y:y+h,x:x+w]
        dist0=((wide*668.748634441)/w)
        actual_dist=dist0*(width/2)/668.748634441
        name='pics\pic'+str(i)+'.png'
        cv2.imwrite(name,crop_img)
        #Main.main(name)
        cv2.imwrite(name,crop_img)
        cv2.imshow("crop",crop_img)
        if flag is True and int(round(center_x)):
            
            start=time.time()
            flag=False
            
            #print("Start:",start)  
        
        if flag is False and int(round(center_x)) in range(int(round(width/2))-10,int(round(width/2))+10):
            end=time.time()
            time_diff=end-start
            #print("End:",end)
            flag=True
            s_flag=True

    if time_diff>0 and s_flag==True:
        velocity=actual_dist/time_diff
        #print(round(start),round(end))
        vel_kmph=round(velocity*3.6,2)
        #print("Speed:",vel_kmph,"kmph")
        #print("Distance from car:",round(dist1,2),"m")
        s_flag=False

      
        if vel_kmph>60:
            TIME.append(str(datetime.datetime.now()))
            VEL.append(vel_kmph)
            
            '''#add email code here my computer its not working
            sender = 'surabhi14kuriyal@gmail.com'
            receivers = ['sarvagyamishra33@gmail.com']
            message="ALERT YOUR SPEED EXCEEDS 10MPH YOU CAN BE CHARGED FURTHER"
            smtpObj = smtplib.SMTP('localhost',25)
            smtpObj.starttls()
            smtp.login(sender,'')
            smtpObj.sendmail(sender, receivers, message)         
            print ("Successfully sent email")'''
        

       
    cv2.imshow('video', img)
    #cv2.imwrite('messigray.png',c)
    key = cv2.waitKey(1) & 0xFF
    if key == ord("q"):
        break
    ret, img = cap.read()
EMail=['emailexample@gmail.com']*len(VEL)
Phone=["989909xxxx"]*len(VEL)
ID=['UK07-'+str(i) for i in range(0,len(VEL))]
newdf=pd.DataFrame({'ID':ID,'Time':TIME,'Velocity':VEL,'E-Mail':EMail,'Phone':Phone})
newdf.to_csv('Defaulters.csv')
cv2.destroyAllWindows()

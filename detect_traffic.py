# -*- coding: utf-8 -*-

import cv2
import sys 
import os
import numpy
import time
import subprocess as sp
import serial



cascade_src = 'cars.xml'
CASCADE_SRC = 'cars.xml'
video_src = 'dataset/l_road.mov'
video_src_2 = 'dataset/r_road.mov'
video_src_3 = 'dataset/m_road.mov'

VIDEO_URL = 'http://konya.sehirkameralari.com/live/594b8c7fc023a/playlist.m3u8'

# 1 -> ana yolu kırmızı->yeşile
# 2 -> ana yolu yeşilden->kırmızıya
# 0 -> ikisi de kırmızı
# 3 -> ikinci yol kırımızı -> yeşile
# 4 -> ikinci yol yeşil -> kırmızıya

serialport = serial.Serial('/dev/cu.wchusbserial1420', 9600)
time.sleep(3)
cap = cv2.VideoCapture(video_src)
cap_2 = cv2.VideoCapture(video_src_2)
cap_3 = cv2.VideoCapture(video_src_3)


car_cascade = cv2.CascadeClassifier(cascade_src)

def detect_live():
    print("[DEBUG]: INIT")
    print("[DEBUG]: FFMPEG SETTED")
    pipe = sp.Popen(["ffmpeg", "-i", VIDEO_URL,
                     "-loglevel", "quiet",  # no text output
                     "-an",  # disable audio
                     "-f", "image2pipe",
                     "-pix_fmt", "yuvj420p",
                     "-vcodec", "rawvideo", "-"],
                    stdin=sp.PIPE, stdout=sp.PIPE)

    print("[DEBUG]: DETECTION TRIGGERED FROM LIVE CAM")
    
    while True:
        # reading the raw data from stdout
        raw_image = pipe.stdout.read(1080 * 1920 * 3)

        # shaping the array to a image format
        image = numpy.fromstring(raw_image, dtype='uint8').reshape(1080, 1920, 3)
        
        # crop the image and get rid of the redundant frames
        image = image[0:360, 0:640] # .copy()
        image = cv2.resize(image, (640, 360))

        image1 = image.copy()
        image2 = image.copy()
        
        left_area = image1[0:240, 0:360].copy()        
        right_area = image2[156:396, 225:585].copy()
        
        # gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        # car_cascade = cv2.CascadeClassifier(CASCADE_SRC)
        # cars = car_cascade.detectMultiScale(gray, 1.1, 1)

        gray1 = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        car_cascade1 = cv2.CascadeClassifier(CASCADE_SRC)
        cars1 = car_cascade1.detectMultiScale(gray1, 1.1, 1)

        left_area_gray = cv2.cvtColor(left_area, cv2.COLOR_BGR2GRAY)
        car_cascade = cv2.CascadeClassifier(CASCADE_SRC)
        cars_on_left = car_cascade.detectMultiScale(left_area_gray, 1.1, 1)

        right_area_gray = cv2.cvtColor(right_area, cv2.COLOR_BGR2GRAY)
        car_cascade = cv2.CascadeClassifier(CASCADE_SRC)
        cars_on_right = car_cascade.detectMultiScale(right_area_gray, 1.1, 1)

        number_of_cars_on_left = int(len(cars_on_left))
        number_of_cars_on_right = int(len(cars_on_right))

        if number_of_cars_on_left + 1 > number_of_cars_on_right:
            serialport.write(b'1')
        
        if number_of_cars_on_left < number_of_cars_on_right:
            serialport.write(b'3')


        # number_of_cars = int(len(cars))
        # print("Detected: " + str(number_of_cars) + " cars.")

        number_of_cars1 = int(len(cars1))
        # print("Detected: " + str(number_of_cars1) + " cars.")


        # for (x, y, w, h) in cars:
        #     cv2.rectangle(image, (x, y), (x + w, y + h), (0, 0, 255), 2)

        # for (x, y, w, h) in cars1:
        #     # blue
        #     cv2.rectangle(image1, (x, y), (x + w, y + h), (255, 0, 0), 2)
        #     cv2.rectangle(image, (x, y), (x + w, y + h), (255, 0, 0), 2)


        for (x, y, w, h) in cars_on_right:
            # blue
            cv2.rectangle(image, (x+225, y+156), (x+w+225, y+h+156), (255, 0, 0), 2)

        for (x, y, w, h) in cars_on_left:
            # red 
            cv2.rectangle(image, (x, y), (x + w, y + h), (0, 0, 255), 2)

        # render it to the screen
        font = cv2.FONT_HERSHEY_SIMPLEX

        # image = cv2.resize(image, None, fx = 0.5, fy = 0.5, interpolation = cv2.INTER_CUBIC)
        cv2.putText(image, '# of Cars on Left: ' + str(number_of_cars_on_left), (10, 20), font, 0.8, (0, 0, 255), 2, cv2.LINE_AA)
        cv2.imshow("Konya - Detect Left Side", image)
        cv2.moveWindow("Konya - Detect Left Side", 100, 100)

        cv2.putText(image1, '# of Cars on Right: ' + str(number_of_cars_on_right), (10, 20), font, 0.8, (255, 0, 0), 2, cv2.LINE_AA)
        # cv2.imshow("Konya - Detect Right Side", image1)
        # cv2.moveWindow("Konya - Detect Right Side", 900, 100)
        
        # cv2.imshow("Konya - Raw Video", image2)

        # cv2.imshow("Left Area (Cropped)", left_area)
        # cv2.imshow("Right Area (Cropped)", right_area)
        
        if number_of_cars_on_left != number_of_cars1:
            # print("[DEBUG]: DIFFER!")
            pass


        if cv2.waitKey(5) == 27:
            break

    cv2.destroyAllWindows()

def detect_record():
    print("[DEBUG]: INIT")
    print("[DEBUG]: DETECTION TRIGGERED FROM RECORD")
    print("[DEBUG]: OpenCV Version: " + str(cv2.__version__))
    send_to_first_road = b'4'
    first_road_state = b'0'
    time.sleep(3)
    while True:
        start_time = time.time()
        _, img = cap.read()
        _, img2 = cap_2.read()
        _, img3 = cap_3.read()

        if (type(img) == type(None) or type(img2) == type(None)):
            print("break")
            break
        
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        gray_2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
        gray_3 = cv2.cvtColor(img3, cv2.COLOR_BGR2GRAY)

        cars = car_cascade.detectMultiScale(gray, 1.1, 1)
        cars2 = car_cascade.detectMultiScale(gray_2, 1.1, 1)
        cars3 = car_cascade.detectMultiScale(gray_3, 1.1, 1)

        number_of_cars_left = len(cars)
        number_of_cars_right = len(cars2)
        
        if number_of_cars_left + 1 > number_of_cars_right:
            serialport.write(b'1')
        
        if number_of_cars_left < number_of_cars_right:
            serialport.write(b'3')

        # if(send_to_first_road != first_road_state):
        #    first_road_state = send_to_first_road
        
        # left_cars = 0 -init
        # right_cars = 0 -init
        '''
        case 1: sleep işini düşün.
            
            if(left_cars == right_cars == 0):
                tickets 2 - 4
            if(left_cars == right_cars):
                ticket 1
            if left_cars > right_cars and timer_still_have_time:
                    if right_cars == 0
                        timer = begining_count             
                    ticket_1
                    timer--
            if right_cars > left_cars and timer_still_have_time:
                    if left_cars == 0
                        timer = begining_count
                    ticket 3
                    timer --
                
        
        '''
        # serialport.write(b'1')
        # serialport.write(b'3')

        # print("Detected: " + str(len(cars)) + " cars.")
        for (x,y,w,h) in cars:
            cv2.rectangle(img,(x,y),(x+w,y+h),(0,0,255),2)    
            
        for (x,y,w,h) in cars2:
            cv2.rectangle(img2,(x,y),(x+w,y+h),(255,0,0),2)    

        font = cv2.FONT_HERSHEY_SIMPLEX

        cv2.putText(img, '# of Cars on Left: ' + str(number_of_cars_left), (10, 20), font, 0.65, (0, 0, 255), 2, cv2.LINE_AA)
        cv2.imshow('Left Side', img)
        
        cv2.putText(img2, '# of Cars on Left: ' + str(number_of_cars_right), (10, 20), font, 0.65, (255, 0, 0), 2, cv2.LINE_AA)
        cv2.imshow('Right Side', img2)
        
        cv2.imshow('Raw Video', img3)

        cv2.moveWindow('Left Side', 100, 100)
        cv2.moveWindow('Right Side', 800, 100)
        cv2.moveWindow('Raw Video', 450, 600)
        print("FPS: ", 1.0 / (time.time() - start_time))

        if cv2.waitKey(5) == 27:
            # serialport.flush()
            break
    cv2.destroyAllWindows() 


if __name__ == "__main__":
    if len(sys.argv) == 1:
        print("Usage: python detect_traffic.py [live]|[record]")
        sys.exit(0)
    if str(sys.argv[1]) == "live":
        detect_live()
    elif str(sys.argv[1]) == "record":
        detect_record()
    else:
        print("Usage: python detect_traffic.py [live]|[record]")
        sys.exit(0)
    print("[DEBUG]: STOP[!]")

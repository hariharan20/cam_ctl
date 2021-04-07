#! /usr/bin/env python

from std_msgs.msg import String
import rospy
import cv2
from geometry_msgs.msg import Twist
import numpy as np 
rospy.init_node('cam_node')
pub = rospy.Publisher('cam_location' , String , queue_size = 10 )
rate = rospy.Rate(2)

msg_str = String()
cap = cv2.VideoCapture(0)

params = cv2.SimpleBlobDetector_Params()

params.filterByColor = False
params.filterByArea = True
params.minArea = 100
params.maxArea = 3000
params.filterByInertia = False
params.filterByConvexity = False
params.filterByCircularity = True
params.minCircularity = 0.2
params.maxCircularity = 1

det = cv2.SimpleBlobDetector_create(params)

lower_flo = np.array([22 , 120 , 120])
upper_flo = np.array([50 , 255 ,255])

x = True
while not rospy.is_shutdown() :
    
        ret , framev = cap.read()
        frame = cv2.flip(framev , 1)
        imgHSV = cv2.cvtColor(frame , cv2.COLOR_BGR2HSV)

        mask = cv2.inRange(imgHSV , lower_flo, upper_flo)
        blur = cv2.blur(mask , (10 ,10))
        res = cv2.bitwise_and(frame , frame , mask = mask)
        h , w , chan = np.shape(frame)
        key_pts = det.detect(mask)
        cv2.drawKeypoints(res , key_pts , res , (0 , 0 , 255),
        cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
        cv2.line(img=res, pt1=(0 , h/3), pt2=(w , h/3), color=(255, 0, 0), thickness=5, lineType=8, shift=0)
        cv2.line(img=res, pt1=(0 , 2 *h /3), pt2=(w , 2*h/ 3 ), color=(255, 0, 0), thickness=5, lineType=8, shift=0)
        cv2.line(img=res, pt1=(w/3, 0), pt2=(w/3, h), color=(255, 0, 0), thickness=5, lineType=8, shift=0)
        cv2.line(img=res, pt1=(2*w/3, 0), pt2=(2*w/3 , h), color=(255, 0, 0), thickness=5, lineType=8, shift=0)

        #cv2.imshow('img' , frame)
        cv2.imshow('flo' , res)
        #cv2.imshow('flo' , res)

        for k in key_pts :
            if (k.pt[0] >= w/3) & (k.pt[0] <= 2*w/3) & (k.pt[1] < h/3):
                msg_str = 'forward'
        
            elif (k.pt[0] >= w/3) & (k.pt[0] <= 2*w/3) & (k.pt[1] > 2*h/3) :
                msg_str = 'back'
            elif (k.pt[1] >= h/3) & (k.pt[1] <= 2*h/3) & (k.pt[0] < w/3) :
                msg_str = 'left'
            elif (k.pt[1] >= h/3) & (k.pt[1] <= 2*h/3) & (k.pt[0] > 2*w/3) :
                msg_str = 'right'
            elif (k.pt[1] >= h/3) & (k.pt[1] <= 2*h/3) & (k.pt[0] >= w/3) & (k.pt[0] <=2*w/3):
                msg_str = 'stop'
            else :
                msg_str = 'donkey'


         

        if cv2.waitKey(1) & 0xff == ord('q') :
            break

    
        pub.publish(msg_str)
    

    
   
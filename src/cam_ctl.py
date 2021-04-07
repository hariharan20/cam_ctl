#! /usr/bin/env python
#Written by Hariharan <A.H.N>
import rospy
from geometry_msgs.msg import Twist 
from std_msgs.msg import String 

def callback(msg):
    print msg.data
    move = Twist()
    pub = rospy.Publisher('cmd_vel' , Twist , queue_size =10)
    if msg.data =='forward':
        move.linear.x = 0.5
        move.angular.z = 0.0
    elif msg.data == 'back' :
        move.linear.x = -0.5
        move.angular.z = 0.0
    elif msg.data =='left' :
        move.linear.x =0.0
        move.angular.z = 0.5
    elif msg.data == 'right':
        move.linear.x = 0.0
        move.angular.z = -0.5
    elif msg.data == 'stop' :
        move.linear.x =0.0
        move.angular.z = 0.0

    pub.publish(move)
    
if __name__ =='__main__':

    rospy.init_node('Decoder')

    sub  = rospy.Subscriber('/cam_location' , String , callback)

    rospy.spin()

#!/usr/bin/env python
# Software License Agreement (BSD License)
import sys
import rospy
from std_msgs.msg import String, Float64MultiArray
from sensor_msgs.msg import Image
import numpy as np
from cv_bridge import CvBridge
import cv2

import roslib
from visualization_msgs.msg import Marker
from visualization_msgs.msg import MarkerArray
import math



def process_rgb(msg):
    bridge = CvBridge()
    global have_im; have_im = True
    global im; im = bridge.imgmsg_to_cv2(msg)


if __name__ == '__main__':
    publisher = rospy.Publisher('visualization_marker_array', MarkerArray,queue_size=10)
    rospy.init_node('talker', anonymous=True)
    markerArray = MarkerArray()
    rospy.sleep(1)    
    count = 0
    MARKERS_MAX = 100
    while not rospy.is_shutdown():
       marker = Marker()
       # this frame_id can only be map!
       marker.header.frame_id = "map"
       marker.type = marker.SPHERE
       marker.action = marker.ADD
       marker.scale.x = 0.2
       marker.scale.y = 0.2
       marker.scale.z = 0.2
       marker.color.a = 1.0
       marker.color.r = 1.0
       marker.color.g = 1.0
       marker.color.b = 0.0
       marker.pose.orientation.w = 1.0
       marker.pose.position.x = math.cos(count / 50.0)
       marker.pose.position.y = math.cos(count / 40.0) 
       marker.pose.position.z = math.cos(count / 30.0) 

       # We add the new marker to the MarkerArray, removing the oldest
       # marker from it when necessary
       if(count > MARKERS_MAX):
           markerArray.markers.pop(0)

       markerArray.markers.append(marker)

       # Renumber the marker IDs
       id = 0
       for m in markerArray.markers:
           m.id = id
           id += 1

       # Publish the MarkerArray
       publisher.publish(markerArray)
        
       count += 1
       print(count)
       rospy.sleep(0.01)

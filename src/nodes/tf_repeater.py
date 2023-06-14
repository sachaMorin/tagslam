#!/usr/bin/env python3
"""TagSLAM does not update the transforms of dynamic objects that are not in view (e.g., the obstacles). This can
lead the rig to obstacle transforms to be outdated.

This node simply subscribes to obstacle transforms and republishes them with the current time, which allows to get
better current potentials."""
import roslib
import rospy
import tf
import json

import socket
import sys
import json
from std_msgs.msg import String

UDP_IP = "127.0.0.1"
UDP_PORT = 5005

if __name__ == '__main__':
    sock = socket.socket(socket.AF_INET,  # Internet
                         socket.SOCK_DGRAM)  # UDP

    rospy.init_node('tf_repeater')
    listener = tf.TransformListener()
    br = tf.TransformBroadcaster()

    rate = rospy.Rate(30)
    while not rospy.is_shutdown():
        message = dict()

        # Lookup required transforms
        for obj in ['/obstacle1', '/obstacle2', '/obstacle3', '/obstacle4']:
            try:
                (trans,rot) = listener.lookupTransform('/odom', obj, rospy.Time(0))
            except (tf.LookupException, tf.ConnectivityException, tf.ExtrapolationException):
                continue
            br.sendTransform(trans,
                             rot,
                             rospy.Time.now(),
                             "odom",
                             obj)

        rate.sleep()

    # Close socket
    sock.close()

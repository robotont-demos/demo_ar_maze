#!/usr/bin/python
'''
Run these to start maze navigation:
roslaunch ar_maze_robotont test_world.launch
roslaunch ar_maze_robotont ar_maze_robotont.launch
'''

import numpy
import rospy
import time

from ar_track_alvar_msgs.msg import AlvarMarkers
from geometry_msgs.msg import Twist


def stop_robot():
    global vel_msg, velocity_publisher
    vel_msg.linear.x = 0
    vel_msg.angular.z = 0
    velocity_publisher.publish(vel_msg)


def markers_callback(data):
    global dist, marker_id, vel_msg, velocity_publisher, state, next_marker

    for marker in data.markers:
        dist = marker.pose.pose.position.x # Distance from the marker
        rospy.loginfo("dist: " + str(dist))
        marker_id = marker.id
        rospy.loginfo('Marker id: ' + str(marker_id))

    if state == "searching":
        vel_msg.linear.x = 0

        if len(data.markers) > 0 and data.markers[0].id == next_marker:
            rospy.loginfo("data.markers[0].id: " + str(data.markers[0].id))
            state = "centering"
            vel_msg.angular.z = 0
            rospy.loginfo("state: " + state + "; next_marker:" + str(next_marker))

        else:
            vel_msg.angular.z = 0.6


    elif state == "centering":
        vel_msg.linear.x = 0

        if len(data.markers) > 0:
            if marker.pose.pose.position.y < -0.1:
                vel_msg.angular.z = -0.3
            elif marker.pose.pose.position.y > 0.1:
                vel_msg.angular.z = 0.3
            else:
                state = "following"
                vel_msg.angular.z = 0
                rospy.loginfo("state: " + state + "; next_marker:" + str(next_marker))

        else: # If robot loses the marker due to it being too far
            rospy.loginfo("dist:" + str(dist))
            if dist > 1:
                vel_msg.linear.x = 0.5
                vel_msg.angular.z = 0
            else:
                vel_msg.linear.x = 0
                vel_msg.angular.z = 0.5


    elif state == "following":
        if dist > 1.0:
            vel_msg.linear.x = 0.5
        else:
            vel_msg.linear.x = 0
            next_marker = marker_id + 1
            state = "searching"
            rospy.loginfo("state: " + state + "; next_marker:" + str(next_marker))

            if next_marker == 6:
                rospy.signal_shutdown("Maze completed")


def main():
    global vel_msg, velocity_publisher, state, next_marker

    rospy.init_node('robotont_velocity_publisher', anonymous=True, disable_signals = True)
    rospy.loginfo('Subscribing to ar_pose_marker')
    rospy.Subscriber('ar_pose_marker', AlvarMarkers, markers_callback)

    velocity_publisher = rospy.Publisher('cmd_vel', Twist, queue_size=10)

    vel_msg = Twist()
    vel_msg.linear.x = 0
    vel_msg.linear.y = 0
    vel_msg.linear.z = 0
    vel_msg.angular.x = 0
    vel_msg.angular.y = 0
    vel_msg.angular.z = 0

    next_marker = 1

    state = "searching"

    while not rospy.is_shutdown():
        time.sleep(0.1)
        #rospy.loginfo("vel_msg.linear.x: " + str(vel_msg.linear.x) + "; dist: " + str(dist))

        velocity_publisher.publish(vel_msg)

        rospy.on_shutdown(stop_robot)


if __name__ == "__main__":
    main()
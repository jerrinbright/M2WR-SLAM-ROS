#! /usr/bin/env python
import rospy
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist

def action(regions):
    global pub
    data = Twist()
    linear_x = 0
    angular_z = 0

    state_description = ''

    if regions['front'] > 1 and regions['fleft'] > 1 and regions['fright'] > 1:
        state_description = 'case 1'
        linear_x = 0.6
        angular_z = 0
    elif regions['front'] < 1 and regions['fleft'] > 1 and regions['fright'] > 1:
        state_description = 'case 2'
        linear_x = 0
        angular_z = -0.3
    elif regions['front'] > 1 and regions['fleft'] > 1 and regions['fright'] < 1:
        state_description = 'case 3'
        linear_x = 0
        angular_z = -0.3
    elif regions['front'] > 1 and regions['fleft'] < 1 and regions['fright'] > 1:
        state_description = 'case 4'
        linear_x = 0
        angular_z = 0.3
    elif regions['front'] < 1 and regions['fleft'] > 1 and regions['fright'] < 1:
        state_description = 'case 5'
        linear_x = 0
        angular_z = -0.3
    elif regions['front'] < 1 and regions['fleft'] < 1 and regions['fright'] > 1:
        state_description = 'case 6'
        linear_x = 0
        angular_z = 0.3
    elif regions['front'] < 1 and regions['fleft'] < 1 and regions['fright'] < 1:
        state_description = 'case 7'
        linear_x = 0
        angular_z = -0.3
    elif regions['front'] > 1 and regions['fleft'] < 1 and regions['fright'] < 1:
        state_description = 'case 8'
        linear_x = 0
        angular_z = -0.3
    else:
        state_description = 'unknown case'
        rospy.loginfo(regions)

    rospy.loginfo(state_description)
    data.linear.x = linear_x
    data.angular.z = angular_z
    pub.publish(data)


def callback(data):
    global regions
    regions={
        'right':min(min(data.ranges[0:143]), 10),
        'fright'  :min(min(data.ranges[144:287]), 10),
        'front'  :min(min(data.ranges[288:431]), 10),
        'fleft'   :min(min(data.ranges[432:575]), 10),
        'left' :min(min(data.ranges[576:713]), 10),
    }
    action(regions)

rospy.init_node("obstacle_avoidance")
global pub
pub = rospy.Publisher('/cmd_vel', Twist, queue_size=1)
sub=rospy.Subscriber("/m2wr/laser/scan",LaserScan,callback)
rospy.spin()
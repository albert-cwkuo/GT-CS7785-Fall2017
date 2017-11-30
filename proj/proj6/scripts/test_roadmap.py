#!/usr/bin/env python2
import rospy
from kuo_proj6.srv import GetKnnNode, GetKnnNodeResponse, GetNextWaypoints, InitMap
from geometry_msgs.msg import Point

rospy.init_node('test_roadmap')
rospy.wait_for_service('/get_knn_node')
get_knn_client = rospy.ServiceProxy('/get_knn_node', GetKnnNode)
query = Point()
query.x = -0.1
query.y= 1.15
resp = get_knn_client(query, 2)
print(resp)
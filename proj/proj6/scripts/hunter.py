#!/usr/bin/env python2
import rospy
from enum import Enum
from kuo_proj6.srv import GetKnnNode, GetKnnNodeResponse, GetNextWaypoints, InitMap
from actionlib_msgs.msg import GoalStatus
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
import tf
import actionlib
from time import sleep
from geometry_msgs.msg import Point

class States(Enum):
    INIT=0
    BRANCH=1
    GO=2
    GOAL=3

class Hunter:
    def __init__(self):
        rospy.init_node('hunter')
        # request roadmap node's services
        rospy.wait_for_service('/get_knn_node')
        self.get_knn_client = rospy.ServiceProxy('/get_knn_node', GetKnnNode)
        # subscribe to move_base's action server
        self.move_base_ac = actionlib.SimpleActionClient('/move_base', MoveBaseAction)
        self.move_base_ac.wait_for_server()
        # listen to tf
        self.tf_listener = tf.TransformListener()
        sleep(1)
        
        self.state = States.INIT
    
    def run(self):
        if self.state == States.INIT:
            # find the nearest node in the map
            (pos, ori) = self.tf_listener.lookupTransform('/map', '/base_footprint', rospy.Time(0))
            query = Point()
            query.x = pos[0]
            query.y = pos[1]
            resp = self.get_knn_client(query, 2)
            # init map with that nearest node
            # go to that nearest node
            for pose in resp.knn.poses:
                goal = MoveBaseGoal()
                goal.target_pose.header.frame_id = '/map'
                goal.target_pose.header.stamp = rospy.Time.now()
                goal.target_pose.pose.position = pose.position
                goal.target_pose.pose.orientation.x = ori[0]
                goal.target_pose.pose.orientation.y = ori[1]
                goal.target_pose.pose.orientation.z = ori[2]
                goal.target_pose.pose.orientation.w = ori[3]
                self.move_base_ac.send_goal(goal)
                self.move_base_ac.wait_for_result()
            
        elif self.state == States.BRANCH:
            pass
        elif self.state == States.GO:
            pass
        elif self.state == States.GOAL:
            pass
            

if __name__ == "__main__":
    hunter = Hunter()
    hunter.run()
    
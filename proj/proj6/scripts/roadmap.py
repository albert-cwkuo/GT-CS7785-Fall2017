#!/usr/bin/env python2
import rospy
from kuo_proj6.srv import GetKnnNode, GetKnnNodeResponse, GetNextWaypoints, InitMap
from nav_msgs.srv import GetPlan
import tf
import numpy as np
import scipy.io as sio
from geometry_msgs.msg import PoseStamped, Pose
import argparse

ROBOT_FRAME = '/base_footprint'
MAP_FRAME = '/map'

class Roadmap:
    def __init__(self, map_path):
        rospy.init_node('roadmap')
        # subscribe tf
        self.tf_listener = tf.TransformListener()
        # request service
        rospy.wait_for_service('/move_base/make_plan')
        self.get_plan_client = rospy.ServiceProxy('/move_base/make_plan', GetPlan)
        # provide service
        self.get_knn_node_server = rospy.Service('/get_knn_node', GetKnnNode, self.get_knn_node)
        self.init_map_server = rospy.Service('/init_map', GetNextWaypoints, self.init_map)
        self.get_next_waypoints_server = rospy.Service('/get_next_waypoints', InitMap, self.get_next_waypoints)
        self.map_graph = self.loadRoadmap(map_path)
        
    def loadRoadmap(self, map_path):
        map_graph_mat = sio.loadmat(map_path)['map_graph']
        num_nodes = map_graph_mat.shape[0]
        map_graph = dict()
        for i in range(num_nodes):
            pos = map_graph_mat[i][0].squeeze()
            neighbors = map_graph_mat[i][1].squeeze()
            map_graph[i+1] = {'pos':pos, 'neighbors':neighbors}
        return map_graph
        
    def get_knn_node(self, req):
        rospy.loginfo('get_knn_node service requested')
        k=req.k
        start = PoseStamped()
        start.header.frame_id = '/map'
        start.header.stamp = rospy.Time.now()
        start.pose.position = req.query
        start.pose.orientation.x = 0
        start.pose.orientation.y = 0
        start.pose.orientation.z = 0
        start.pose.orientation.w = 1
        
        dist_all = dict()
        for key, value in self.map_graph.items():
            # get gloabl path
            goal = PoseStamped()
            goal.header.frame_id = '/map'
            goal.header.stamp = rospy.Time.now()
            goal.pose.position.x = value['pos'][0]
            goal.pose.position.y = value['pos'][1]
            goal.pose.position.z = 0
            goal.pose.orientation.x = 0
            goal.pose.orientation.y = 0
            goal.pose.orientation.z = 0
            goal.pose.orientation.w = 1
            resp = self.get_plan_client(start, goal, 0.1)
            waypts = resp.plan.poses
            # compute path length
            dx=waypts[0].pose.position.x-req.query.x
            dy=waypts[0].pose.position.y-req.query.y
            path_length = np.linalg.norm([dx,dy])
            for i in range(1, len(waypts)):
                dx=waypts[i].pose.position.x-waypts[i-1].pose.position.x
                dy=waypts[i].pose.position.y-waypts[i-1].pose.position.y
                path_length += np.linalg.norm([dx,dy])
            dist_all[path_length]=key
        # find k nearest nodes
        dist = dist_all.keys()
        dist.sort()
        resp = GetKnnNodeResponse()
        for d in dist[:k]:
            p = Pose()
            p.position.x = self.map_graph[dist_all[d]]['pos'][0]
            p.position.y = self.map_graph[dist_all[d]]['pos'][1]
            resp.knn.poses.append(p)
            print(p.position)
        return resp
    
    def init_map(self, req):
        pass
    
    def get_next_waypoints(self, req):
        pass
    
    def run(self):
        rospy.spin()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Roadmap node')
    parser.add_argument('--map-path', type=str, metavar='PATH',
                        help='path to the parsed map graph file')
    args = parser.parse_args()
    
    roadmap = Roadmap(args.map_path)
    roadmap.run()
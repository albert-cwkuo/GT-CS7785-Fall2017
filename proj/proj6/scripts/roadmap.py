#!/usr/bin/env python2
import rospy

ROBOT_POSE_TOPIC

class Roadmap:
    def __init__(self):
        rospy.init_node('roadmap')
        get_knn_node = rospy.Service('get_knn_node', TBD, self.get_knn_node)
        init_graph = rospy.Service('init_graph', TBD, self.init_graph)
        get_next_nodes = rospy.Service('get_next_nodes', TBD, self.get_next_nodes)
    
    def get_knn_node(self, req):
        pass
    
    def init_graph(self, req):
        pass
    
    def get_next_nodes(self, req):
        pass
    
    def run(self):
        pass


if __name__ == "__main__":
    roadmap = Roadmap()
    roadmap.run()
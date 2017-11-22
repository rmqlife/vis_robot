import sys
import copy
import rospy
import moveit_commander
import moveit_msgs.msg
import geometry_msgs.msg
from visualization_msgs.msg import Marker, MarkerArray


import sys
import rospy
from std_msgs.msg import String, Float64MultiArray
from sensor_msgs.msg import Image
import numpy as np
import roslib
from visualization_msgs.msg import Marker
from visualization_msgs.msg import MarkerArray
import math


## END_SUB_TUTORIAL
def cloth():   
    print "marker"
    pub = rospy.Publisher('visualization_marker', Marker, queue_size=10)
    rospy.sleep(1)    
    count = 0
    MARKERS_MAX = 100
    while not rospy.is_shutdown():
       marker = Marker()
       # this frame_id can only be map!
       marker.header.frame_id = "odom_combined"
       marker.type = marker.MESH_RESOURCE
       marker.mesh_resource = 'package://pr2_moveit_config/1117-1049/'+format(count,'04d')+'.stl'
       marker.action = marker.ADD
       marker.scale.x = 1
       marker.scale.y = 1
       marker.scale.z = 1
       marker.color.a = 1.0
       marker.color.r = 1.0
       marker.color.g = 1.0
       marker.color.b = 0.0
       marker.pose.orientation.w = 1
       marker.pose.orientation.x = 0
       marker.pose.orientation.y = 0       
       marker.pose.orientation.z = -1
       
       marker.pose.position.x = 0.5
       marker.pose.position.y = 0.5 
       marker.pose.position.z = 1.2
       # Publish the MarkerArray
       pub.publish(marker)
       count += 1
       print(count)
       rospy.sleep(0.02)
       
from std_msgs.msg import String
def pose_msg(p):
    a = geometry_msgs.msg.Pose()
    a.orientation.w = p[0]
    a.position.x = p[1]
    a.position.y = p[2]
    a.position.z = p[3]
    return a

def handle_to_pos(h):
    print h
    pose1 = [1, h[1]+0.5, h[0]-0.5,  h[2]+1.2]
    pose2 = [1, h[4]+0.5, h[3]-0.5,  h[5]+1.2]
    print pose1, pose2
    right = pose_msg(pose1)
    left = pose_msg(pose2)
    return left,right

def move():
    print "============ Starting tutorial setup"
    moveit_commander.roscpp_initialize(sys.argv)
    rospy.init_node('move_group_python_interface_tutorial',
                  anonymous=True)
    robot = moveit_commander.RobotCommander()
    scene = moveit_commander.PlanningSceneInterface()
    ## Instantiate a MoveGroupCommander object.  This object is an interface
    ## to one group of joints.  In this case the group is the joints in the left
    ## arm.
    group = moveit_commander.MoveGroupCommander("arms")
    
    traj_pub = rospy.Publisher('/move_group/display_planned_path',moveit_msgs.msg.DisplayTrajectory,queue_size=20)                            
    scene_pub = rospy.Publisher('/planning_scene',moveit_msgs.msg.PlanningScene,queue_size=20)

    ## Wait for RVIZ to initialize. This sleep is ONLY to allow Rviz to come up.
    # print robot.get_current_state()
    
    fn = '/home/rmqlife/work/gamma48c/cloth2/1117-1049/data.npz'
    import numpy as np
    handles = np.load(fn)['tt_handles']
    print handles.shape
    display_trajectory = moveit_msgs.msg.DisplayTrajectory()

    for i in range(1000):
        display_trajectory.trajectory_start = robot.get_current_state()
        left,right = handle_to_pos(handles[i,:6].tolist())
        group.set_pose_target(left, 'l_wrist_roll_link')
        group.set_pose_target(right, 'r_wrist_roll_link')
        ## Now, we call the planner to compute the plan
        ## and visualize it if successful
        plan1 = group.plan()
        ## You can ask RVIZ to visualize a plan (aka trajectory) for you.  But the
        ## group.plan() method does this automatically so this is not that useful
        ## here (it just displays the same trajectory again).
        print "============ Visualizing plan1"
        group.execute(plan1)
        rospy.sleep(1)
        
    display_trajectory.trajectory.append(plan1)
    traj_pub.publish(display_trajectory)
    
    
    cloth()
if __name__=='__main__':
    try:
        move()
    except rospy.ROSInterruptException:
        pass


#
# Requirements:
#  * Isaac simulator
#  * isaac_ros_image_proc
#  * isaac_ros_stereo_image_proc
#  * nav2_bringup
#  * isaac_ros_visual_slam (optional, for vo:=isaac)
# 
# 1. Launch Isaac Simulator
#
# 2. Open Isaac Examples -> ROS2 -> Navigation -> Carter Navigation (or iw.hub Navigation, for more visual features)
# 
# 3. Enable front stereo right camera:
#   In the Stage tab, open World->Nova_Carter_ROS->front_hawk->right_camera_render_product, 
#   then under Property->Isaac Create Render Product Node->Inputs, check "Enabled". To make
#   simulation faster, set height=600 and width=960. Do the same for the front stereo left camera.
#   
# 4. Make sure that after you click on Play button in the simulator, you can see these topics:
#   $ ros2 topic list
#   /front_stereo_camera/left/camera_info
#   /front_stereo_camera/left/image_raw
#   /front_stereo_camera/left/image_raw/nitros_bridge
#   /front_stereo_camera/right/camera_info
#   /front_stereo_camera/right/image_raw
#   /front_stereo_camera/right/image_raw/nitros_bridge
#   /front_stereo_imu/imu
#
# 5. Launch the example:
#   $ ros2 launch rtabmap_demos isaac_sim_vslam_demo.launch.py
#
# 6. You should be able to send goals in RVIZ to move the robot, or use:
#   $ ros2 run teleop_twist_keyboard teleop_twist_keyboard
#
# === Advanced ===
# With this launch file, we can also experiment with visual odometry with/without disparity computed on GPU.
#
# A. Use RTAB-Map's Visual Odometry:
#   $ ros2 launch rtabmap_demos isaac_sim_vslam_demo.launch.py vo:=rtabmap stereo:=true
#   $ ros2 launch rtabmap_demos isaac_sim_vslam_demo.launch.py vo:=rtabmap stereo:=false
#
# B. Use Isaac Visual Odometry:
#    We should disable wheel odometry TF publishing in the simulator to make it work. To
#    do so, in the Stage tab, open World->Nova_Carter_ROS->transform_tree_odometry->ros2_publish_raw_transform_tree,
#    then under Property->ROS2Publish Raw Transform Tree Node->Inputs, change topicName from "tf" to "tf_odom_ignored".
#   $ ros2 launch rtabmap_demos isaac_sim_vslam_demo.launch.py vo:=isaac stereo:=true
#   $ ros2 launch rtabmap_demos isaac_sim_vslam_demo.launch.py vo:=isaac stereo:=false
#
#

from ament_index_python.packages import get_package_share_directory

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription, OpaqueFunction
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution
from launch_ros.actions import ComposableNodeContainer
from launch_ros.descriptions import ComposableNode

def launch_setup(context, *args, **kwargs):
    # Directories
    pkg_nav2_bringup = get_package_share_directory(
        'nav2_bringup')
    pkg_rtabmap_demos = get_package_share_directory(
        'rtabmap_demos')
    pkg_rtabmap_isaacsim_d455 = get_package_share_directory(
        'rtabmap_isaacsim_d455')

    # Paths
    nav2_launch = PathJoinSubstitution(
        [pkg_nav2_bringup, 'launch', 'navigation_launch.py'])
    nav2_vo_params = PathJoinSubstitution(
        [pkg_rtabmap_demos, 'params', 'isaac_vslam_nav2_params.yaml'])
    nav2_params = PathJoinSubstitution(
        [pkg_rtabmap_demos, 'params', 'isaac_nav2_params.yaml'])
    rviz_launch = PathJoinSubstitution(
        [pkg_nav2_bringup, 'launch', 'rviz_launch.py'])
    rtabmap_launch = PathJoinSubstitution(
        [pkg_rtabmap_demos, 'launch', 'isaac', 'isaac_vslam.launch.py'])
    stereo_processing_launch = PathJoinSubstitution(
        [pkg_rtabmap_isaacsim_d455, 'launch', 'stereo_image_processing.launch.py'])
    isaac_vslam_launch = PathJoinSubstitution(
        [pkg_rtabmap_isaacsim_d455, 'launch', 'isaac_visual_slam.launch.py'])
    
    vo = LaunchConfiguration('vo').perform(context)

    # Include stereo image processing launch
    stereo_processing = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([stereo_processing_launch]),
        launch_arguments=[
            ('image_width', LaunchConfiguration('image_width')),
            ('image_height', LaunchConfiguration('image_height'))
        ]
    )
    
    nav2_args = [('use_sim_time', 'true')]
    if vo == 'rtabmap':
        # We need to change the base odom frame to vo
        nav2_args.append(('params_file', str(nav2_vo_params.perform(context))))
    else:
        # Use custom version with higher velocities
        nav2_args.append(('params_file', str(nav2_params.perform(context))))
    nav2 = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([nav2_launch]),
        launch_arguments=nav2_args
    )
    
    rviz = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([rviz_launch])
    )
    
    rtabmap = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([rtabmap_launch]),
        launch_arguments=[
            ('rtabmap_viz', LaunchConfiguration('rtabmap_viz')),
            ('localization', LaunchConfiguration('localization')),
            ('use_sim_time', 'true'),
            ('stereo_camera_namespace', 'front_stereo_camera'),
            ('enable_vo', str(vo == 'rtabmap')),
            ('stereo', LaunchConfiguration('stereo'))
        ]
    )

    # Add actions
    actions = [rtabmap, nav2, rviz, stereo_processing]

    if vo == 'isaac':
        isaac_vslam = IncludeLaunchDescription(
            PythonLaunchDescriptionSource([isaac_vslam_launch])
        )
        actions.append(isaac_vslam)

    return actions

def generate_launch_description():
    return LaunchDescription([
        DeclareLaunchArgument('rtabmap_viz', default_value='true',
                          choices=['true', 'false'], description='Start rtabmap_viz.'),
        DeclareLaunchArgument('localization', default_value='false',
                          choices=['true', 'false'], description='Start rtabmap in localization mode (a map should have been already created).'),
        DeclareLaunchArgument('vo', default_value='none',
                          choices=['none', 'rtabmap', 'isaac'], description='Enable visual odometry using one of the approach. None means only wheel odometry is used. If you set this to "isaac", make sure to disable odom -> base_link if it exists, because isaac will publish on same TF!'),
        DeclareLaunchArgument('stereo', default_value='true',
                          choices=['true', 'false'], description='Use stereo images as input instead of left+depth images.'),
        DeclareLaunchArgument('image_width', default_value='960',
                          description='Resize input images.'),
        DeclareLaunchArgument('image_height', default_value='600',
                          description='Resize input images.'),
        OpaqueFunction(function=launch_setup)
    ])
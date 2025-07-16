# RealSense D455 Stereo SLAM Launch File
# Configures D455 camera for RTAB-Map SLAM with stereo vision and IMU
#
# Requirements:
#   - RealSense D455 camera
#   - realsense2_camera ROS2 package: sudo apt install ros-humble-realsense2-camera
#   - imu_filter_madgwick: sudo apt install ros-humble-imu-filter-madgwick
#
# Usage:
#   ros2 launch rtabmap_isaacsim_d455 realsense_d455_stereo.launch.py
#   ros2 launch rtabmap_isaacsim_d455 rtabmap_main.launch.py d455:=true
#

import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch_ros.actions import Node, SetParameter
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration

def generate_launch_description():
    """
    Launch RealSense D455 with RTAB-Map SLAM configuration
    """
    # RTAB-Map parameters optimized for D455
    rtabmap_parameters = [{
        'frame_id': 'camera_link',
        'subscribe_stereo': True,
        'subscribe_odom_info': True,
        'wait_imu_to_init': True,
        'approx_sync': False,
        'queue_size': 10
    }]

    # Topic remappings for D455 infrared cameras
    topic_remappings = [
        ('imu', '/imu/data'),
        ('left/image_rect', '/camera/infra1/image_rect_raw'),
        ('left/camera_info', '/camera/infra1/camera_info'),
        ('right/image_rect', '/camera/infra2/image_rect_raw'),
        ('right/camera_info', '/camera/infra2/camera_info')
    ]

    return LaunchDescription([
        # === LAUNCH ARGUMENTS ===
        DeclareLaunchArgument(
            'unite_imu_method', 
            default_value='2',
            description='IMU unite method: 0=None, 1=copy, 2=linear_interpolation'
        ),

        # === CAMERA CONFIGURATION ===
        # Disable IR emitter for better stereo performance
        SetParameter(name='depth_module.emitter_enabled', value=0),

        # === REALSENSE D455 CAMERA DRIVER ===
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource([os.path.join(
                get_package_share_directory('realsense2_camera'), 'launch', 'rs_launch.py')]),
            launch_arguments={
                'camera_namespace': '',
                'enable_gyro': 'true',
                'enable_accel': 'true',
                'unite_imu_method': LaunchConfiguration('unite_imu_method'),
                'enable_infra1': 'true',
                'enable_infra2': 'true',
                'enable_sync': 'true'
            }.items(),
        ),

        # === RTAB-MAP VISUAL ODOMETRY ===
        Node(
            package='rtabmap_odom', 
            executable='stereo_odometry', 
            output='screen',
            parameters=rtabmap_parameters,
            remappings=topic_remappings
        ),

        # === RTAB-MAP SLAM ===
        Node(
            package='rtabmap_slam', 
            executable='rtabmap', 
            output='screen',
            parameters=rtabmap_parameters,
            remappings=topic_remappings,
            arguments=['-d']  # Delete database on startup
        ),

        # === RTAB-MAP VISUALIZATION ===
        Node(
            package='rtabmap_viz', 
            executable='rtabmap_viz', 
            output='screen',
            parameters=rtabmap_parameters,
            remappings=topic_remappings
        ),
                
        # === IMU FILTER ===
        # Process raw IMU data from D455
        Node(
            package='imu_filter_madgwick', 
            executable='imu_filter_madgwick_node', 
            output='screen',
            parameters=[{
                'use_mag': False, 
                'world_frame': 'enu', 
                'publish_tf': False
            }],
            remappings=[('imu/data_raw', '/camera/imu')]
        ),
    ])

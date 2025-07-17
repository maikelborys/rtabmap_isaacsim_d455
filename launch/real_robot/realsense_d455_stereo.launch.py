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
    # Get package directory for unified parameters
    pkg_rtabmap_isaacsim_d455 = get_package_share_directory('rtabmap_isaacsim_d455')
    
    # Use unified parameters file for consistency with simulation
    unified_params_file = os.path.join(pkg_rtabmap_isaacsim_d455, 'config', 'nav2_rtabmap_params.yaml')

    # Topic remappings for D455 infrared cameras (stereo mode)
    topic_remappings = [
        ('imu', '/imu/data'),
        ('left/image_rect', '/camera/infra1/image_rect_raw'),
        ('left/camera_info', '/camera/infra1/camera_info'),
        ('right/image_rect', '/camera/infra2/image_rect_raw'),
        ('right/camera_info', '/camera/infra2/camera_info'),
        # Use visual odometry frame
        ('odom', '/camera_odom')
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
                'enable_color': 'false',  # Disable RGB for stereo-only mode
                'enable_depth': 'false',  # Disable depth for stereo-only mode
                'enable_sync': 'true',
                # Optimize for stereo SLAM
                'infra_width': '848',
                'infra_height': '480',
                'infra_fps': '30',
                # Disable emitter for better stereo performance
                'emitter_enabled': '0',
                # Manual exposure for consistent results
                'enable_auto_exposure': 'false',
                'exposure': '8500',
                'gain': '16'
            }.items(),
        ),

        # === RTAB-MAP VISUAL ODOMETRY ===
        Node(
            package='rtabmap_odom', 
            executable='stereo_odometry', 
            output='screen',
            parameters=[{
                'frame_id': 'camera_link',
                'odom_frame_id': 'camera_odom',
                'publish_tf': True,
                'approx_sync': True,
                'queue_size': 50,
                'subscribe_stereo': True,
                'wait_imu_to_init': False,
                'use_sim_time': True
            }],
            remappings=topic_remappings,
            arguments=['--ros-args', '--log-level', 'info']
        ),

        # === RTAB-MAP SLAM ===
        Node(
            package='rtabmap_slam', 
            executable='rtabmap', 
            output='screen',
            parameters=[{
                'frame_id': 'camera_link',
                'odom_frame_id': 'camera_odom', 
                'map_frame_id': 'map',
                'publish_tf': True,
                'approx_sync': True,
                'queue_size': 50,
                'subscribe_stereo': True,
                'subscribe_odom_info': False,  # No wheel odometry
                'use_sim_time': True,
                # Critical RTABMap parameters
                'Vis/MinInliers': '12',
                'Vis/InlierDistance': '0.15',
                'Vis/MaxFeatures': '600',
                'Grid/FromDepth': 'true',
                'Grid/MaxGroundHeight': '0.05',
                'Grid/MinGroundHeight': '-0.05',
                'Grid/GroundIsObstacle': 'false',
                'Reg/Force3DoF': 'true'
            }],
            remappings=topic_remappings,
            arguments=['--delete_db_on_start']  # Clean start
        ),

        # === RTAB-MAP VISUALIZATION (simplified parameters) ===
        Node(
            package='rtabmap_viz', 
            executable='rtabmap_viz', 
            output='screen',
            parameters=[{
                'frame_id': 'camera_link',
                'odom_frame_id': 'camera_odom',
                'map_frame_id': 'map',
                'approx_sync': True,
                'queue_size': 50,
                'subscribe_stereo': True,
                'use_sim_time': True
            }],
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

        # === STATIC TRANSFORMS ===
        # Essential transforms for camera-only SLAM
        Node(
            package='tf2_ros',
            executable='static_transform_publisher',
            name='base_to_camera_link',
            arguments=['0', '0', '0.1', '0', '0', '0', 'base_link', 'camera_link'],
            output='screen'
        ),
        
        # Map to odom transform (identity when using visual SLAM only)
        Node(
            package='tf2_ros',
            executable='static_transform_publisher', 
            name='map_to_odom',
            arguments=['0', '0', '0', '0', '0', '0', 'map', 'camera_odom'],
            output='screen'
        ),
    ])

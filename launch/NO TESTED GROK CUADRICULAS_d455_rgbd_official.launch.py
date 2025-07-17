import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch_ros.actions import Node, SetParameter
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration

def generate_launch_description():
    # Optimized RTAB-Map parameters for dynamic environments
    parameters=[{
        'frame_id': 'camera_link',
        'subscribe_depth': True,
        'subscribe_odom_info': True,
        'approx_sync': False,                    # Exact sync for D455 hardware sync
        'wait_imu_to_init': True,                # Wait for IMU initialization
        # Odometry and feature detection
        'Vis/FeatureType': '6',                  # ORB for robust tracking
        'Vis/MaxFeatures': '2000',               # Increase features for stability
        'Vis/MinInliers': '15',                  # Allow more transformations
        'Vis/InlierDistance': '0.1',             # Tighter inlier distance
        'Reg/Force3DoF': 'true',                 # 2D SLAM constraint
        'RGBD/NeighborLinkRefining': 'true',     # Refine neighbor links
        'RGBD/OptimizeMaxError': '3.0',          # Relax optimization for dynamic scenes
        # Map generation
        'Grid/FromDepth': 'true',                # Generate 2D occupancy grid
        'Grid/MaxObstacleHeight': '2.0',         # Obstacle height limit
        'Grid/MaxGroundHeight': '0.1',           # Ground height tolerance
        'Grid/RayTracing': 'true',               # Clear dynamic objects
        'Grid/3D': 'true',                       # Enable 3D grid for octomap
        'map_always_update': 'true',             # Continuous map updates
        # Debugging
        'Rtabmap/DetectionRate': '2.0',          # 2 Hz for faster feedback
        'Mem/IncrementalMemory': 'true',         # Incremental SLAM
    }]

    # Topic remappings
    remappings=[
        ('imu', '/imu/data'),
        ('rgb/image', '/camera/color/image_raw'),
        ('rgb/camera_info', '/camera/color/camera_info'),
        ('depth/image', '/camera/aligned_depth_to_color/image_raw')
    ]

    return LaunchDescription([
        # Launch arguments
        DeclareLaunchArgument(
            'unite_imu_method', default_value='2',
            description='0-None, 1-copy, 2-linear_interpolation'),
        DeclareLaunchArgument(
            'rgb_profile', default_value='640x480x30',  # Higher resolution
            description='RGB camera profile (640x480x30, 848x480x30, 1280x720x30)'),

        # Camera configuration
        SetParameter(name='depth_module.emitter_enabled', value=1),

        # RealSense D455 driver
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource([os.path.join(
                get_package_share_directory('realsense2_camera'), 'launch'),
                '/rs_launch.py']),
            launch_arguments={
                'camera_namespace': '',
                'device_type': 'd455',
                'enable_color': 'true',
                'rgb_camera.profile': LaunchConfiguration('rgb_profile'),
                'enable_depth': 'true',
                'align_depth.enable': 'true',
                'enable_gyro': 'true',
                'enable_accel': 'true',
                'unite_imu_method': LaunchConfiguration('unite_imu_method'),
                'enable_sync': 'true',
                'enable_infra1': 'false',
                'enable_infra2': 'false',
            }.items(),
        ),

        # Static transform
        Node(
            package='tf2_ros',
            executable='static_transform_publisher',
            name='base_to021_camera',
            arguments=['0', '0', '0', '0', '0', '0', 'base_link', 'camera_link']
        ),

        # RTAB-Map RGBD odometry
        Node(
            package='rtabmap_odom',
            executable='rgbd_odometry',
            name='rgbd_odometry',
            output='screen',
            parameters=parameters,
            remappings=remappings,
            arguments=['--ros-args', '--log-level', 'debug']  # Verbose logging
        ),

        # RTAB-Map SLAM
        Node(
            package='rtabmap_slam',
            executable='rtabmap',
            name='rtabmap',
            output='screen',
            parameters=parameters,
            remappings=remappings,
            arguments=['-d', '--ros-args', '--log-level', 'debug']  # Clear DB, debug
        ),

        # RTAB-Map visualization
        Node(
            package='rtabmap_viz',
            executable='rtabmap_viz',
            name='rtabmap_viz',
            output='screen',
            parameters=parameters,
            remappings=remappings,
            arguments=['--ros-args', '--log-level', 'debug']
        ),

        # IMU filter
        Node(
            package='imu_filter_madgwick',
            executable='imu_filter_madgwick_node',
            name='imu_filter',
            output='screen',
            parameters=[{
                'use_mag': False,
                'world_frame': 'enu',
                'publish_tf': False
            }],
            remappings=[('imu/data_raw', '/camera/imu')]
        ),
    ])
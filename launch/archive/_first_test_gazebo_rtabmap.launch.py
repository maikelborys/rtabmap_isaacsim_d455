#!/usr/bin/env python3 TEST FILE
# hello world TEST FILE
import os
from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        Node(
            package='rtabmap_slam',
            executable='rtabmap',
            name='rtabmap',
            output='screen',
            parameters=[{
                'frame_id': 'base_link',
                'subscribe_depth': True,
                'subscribe_rgb': True,
                'subscribe_scan': False,
                'use_sim_time': True,
                'Rtabmap/DatabasePath': os.path.expanduser('~/rtabmap.db'),
                #'RGBD/ProximityBySpace': True,
                #'Reg/Force3DoF': True,  # 2D mapping
            }],
            remappings=[
                ('rgb/image', '/camera/image_raw'),
                ('rgb/camera_info', '/camera/camera_info'),
                ('depth/image', '/camera/depth/image_raw'),
            ]
        ),
    ])


from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration

def generate_launch_description():
    return LaunchDescription([
        # Declare launch arguments
        DeclareLaunchArgument('namespace', default_value='camera', description='Namespace for camera topics'),

        # RealSense camera node
        Node(
            package='realsense2_camera',
            executable='realsense2_camera_node',
            namespace=LaunchConfiguration('namespace'),
            parameters=[{
                'color_width': '1280',
                'color_height': '720',
                'color_fps': '30.0',
                'depth_width': '1280',
                'depth_height': '720',
                'depth_fps': '30.0',
                'enable_sync': 'true',
                'align_depth.enable': 'true',
                'depth_module.enable_auto_exposure': 'true',
                'temporal_filter.enable': 'true',
                'spatial_filter.enable': 'true',
            }],
            output='screen',
        ),

        # RTAB-Map node
        Node(
            package='rtabmap_ros',
            executable='rtabmap',
            name='rtabmap',
            parameters=[{
                'frame_id': 'camera_link',
                'subscribe_depth': True,
                'subscribe_rgb': True,
                'approx_sync': False,
                'Vis boFeatureType': '6',  # ORB
                'Vis/MaxFeatures': '3000',
                'Vis/MinInliers': '10',
                'Vis/InlierDistance': '0.1',
                'Grid/FromDepth': 'true',
                'Grid/CellSize': '0.05',
                'Grid/RangeMax': '10.0',
                'Grid/RayTracing': 'true',
                'Grid/3D': 'true',
                'map_always_update': 'true',
            }],
            remappings=[
                ('rgb/image', '/camera/color/image_raw'),
                ('depth/image', '/camera/aligned_depth_to_color/image_raw'),
                ('rgb/camera_info', '/camera/color/camera_info'),
            ],
            output='screen',
        ),

        # RTAB-Map visualization
        Node(
            package='rtabmap_ros',
            executable='rtabmap_viz',
            name='rtabmap_viz',
            parameters=[{
                'frame_id': 'camera_link',
                'subscribe_depth': True,
                'subscribe_rgb': True,
                'approx_sync': False,
            }],
            remappings=[
                ('rgb/image', '/camera/color/image_raw'),
                ('depth/image', '/camera/aligned_depth_to_color/image_raw'),
                ('rgb/camera_info', '/camera/color/camera_info'),
            ],
            output='screen',
        ),
    ])
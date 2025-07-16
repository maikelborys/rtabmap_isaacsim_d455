from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import ComposableNodeContainer
from launch_ros.descriptions import ComposableNode
from launch.actions import OpaqueFunction

def launch_setup(context, *args, **kwargs):
    image_width = int(LaunchConfiguration('image_width').perform(context))
    image_height = int(LaunchConfiguration('image_height').perform(context))

    left_resize_node = ComposableNode(
        name='left_resize_node',
        package='isaac_ros_image_proc',
        plugin='nvidia::isaac_ros::image_proc::ResizeNode',
        parameters=[{
            'use_sim_time': True,
            'output_width': image_width,
            'output_height': image_height,
        }],
        namespace="front_stereo_camera",
        remappings=[
            ('image', 'left/image_raw'),
            ('camera_info', 'left/camera_info'),
            ('resize/image', 'left/image_resize'),
            ('resize/camera_info', 'left/camera_info_resize')
        ]
    )

    right_resize_node = ComposableNode(
        name='right_resize_node',
        package='isaac_ros_image_proc',
        plugin='nvidia::isaac_ros::image_proc::ResizeNode',
        parameters=[{
            'use_sim_time': True,
            'output_width': image_width,
            'output_height': image_height,
        }],
        namespace="front_stereo_camera",
        remappings=[
            ('image', 'right/image_raw'),
            ('camera_info', 'right/camera_info'),
            ('resize/image', 'right/image_resize'),
            ('resize/camera_info', 'right/camera_info_resize')
        ]
    )

    left_rectify_node = ComposableNode(
        name='left_rectify_node',
        package='isaac_ros_image_proc',
        plugin='nvidia::isaac_ros::image_proc::RectifyNode',
        parameters=[{
            'use_sim_time': True,
            'output_width': image_width,
            'output_height': image_height,
        }],
        namespace="front_stereo_camera",
        remappings=[
            ('image_raw', 'left/image_resize'),
            ('camera_info', 'left/camera_info_resize'),
            ('image_rect', 'left/image_rect'),
            ('camera_info_rect', 'left/camera_info_rect')
        ]
    )

    right_rectify_node = ComposableNode(
        name='right_rectify_node',
        package='isaac_ros_image_proc',
        plugin='nvidia::isaac_ros::image_proc::RectifyNode',
        parameters=[{
            'use_sim_time': True,
            'output_width': image_width,
            'output_height': image_height,
        }],
        namespace="front_stereo_camera",
        remappings=[
            ('image_raw', 'right/image_resize'),
            ('camera_info', 'right/camera_info_resize'),
            ('image_rect', 'right/image_rect'),
            ('camera_info_rect', 'right/camera_info_rect')
        ]
    )

    disparity_node = ComposableNode(
        name='disparity_node',
        package='isaac_ros_stereo_image_proc',
        plugin='nvidia::isaac_ros::stereo_image_proc::DisparityNode',
        parameters=[{
                'use_sim_time': True,
                'backends': 'CUDA',
                'max_disparity': 64.0
        }],
        namespace="front_stereo_camera",
        remappings=[
            ('left/camera_info', 'left/camera_info_rect'),
            ('right/camera_info', 'right/camera_info_rect'),
        ],
    )
    
    disparity_to_depth_node = ComposableNode(
        name='disparity_to_depth_node',
        package='isaac_ros_stereo_image_proc',
        plugin='nvidia::isaac_ros::stereo_image_proc::DisparityToDepthNode',
        parameters=[{
                'use_sim_time': True,
        }],
        namespace="front_stereo_camera"
    )
    
    stereo_img_proc_container = ComposableNodeContainer(
        name='stereo_img_proc_container',
        package='rclcpp_components',
        namespace="front_stereo_camera",
        executable='component_container_mt',
        composable_node_descriptions=[
            left_resize_node,
            right_resize_node,
            left_rectify_node,
            right_rectify_node,
            disparity_node,
            disparity_to_depth_node
        ],
        output='screen',
        arguments=['--ros-args', '--log-level', 'info',
                   '--log-level', 'color_format_convert:=info',
                   '--log-level', 'NitrosImage:=info',
                   '--log-level', 'NitrosNode:=info'
                   ],
    )
    
    return [stereo_img_proc_container]

def generate_launch_description():
    return LaunchDescription([
        DeclareLaunchArgument('image_width', default_value='960',
                          description='Resize input images.'),
        DeclareLaunchArgument('image_height', default_value='600',
                          description='Resize input images.'),
        OpaqueFunction(function=launch_setup)
    ]) 
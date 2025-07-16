from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch_ros.actions import ComposableNodeContainer
from launch_ros.descriptions import ComposableNode

def generate_launch_description():
    isaac_visual_slam_node = ComposableNode(
        name='visual_slam_node',
        package='isaac_ros_visual_slam',
        plugin='nvidia::isaac_ros::visual_slam::VisualSlamNode',
        remappings=[('visual_slam/image_0', 'front_stereo_camera/left/image_rect'),
                    ('visual_slam/camera_info_0', 'front_stereo_camera/left/camera_info_rect'),
                    ('visual_slam/image_1', 'front_stereo_camera/right/image_rect'),
                    ('visual_slam/camera_info_1', 'front_stereo_camera/right/camera_info_rect')],
        parameters=[{
                    'use_sim_time': True,
                    'enable_image_denoising': True,
                    'enable_planar_mode': True,
                    'rectified_images': True,
                    'publish_map_to_odom_tf': False,
                    'odom_frame': 'odom',
                    'enable_slam_visualization': True,
                    'enable_observations_view': True,
                    'enable_landmarks_view': True}]
    )
    
    isaac_vslam_container = ComposableNodeContainer(
        name='isaac_visual_slam_container',
        namespace='',
        package='rclcpp_components',
        executable='component_container',
        composable_node_descriptions=[isaac_visual_slam_node],
        output='screen',
    )

    return LaunchDescription([
        isaac_vslam_container
    ]) 
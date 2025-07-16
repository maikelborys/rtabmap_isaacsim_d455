# Main launch file for RTAB-Map SLAM system
# Supports both Isaac Sim simulation and RealSense D455 camera
# 
# Usage:
#   Simulation: ros2 launch rtabmap_isaacsim_d455 rtabmap_main.launch.py
#   Real robot: ros2 launch rtabmap_isaacsim_d455 rtabmap_main.launch.py d455:=true
#

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription, OpaqueFunction
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution
from ament_index_python.packages import get_package_share_directory
from launch.launch_description_sources import PythonLaunchDescriptionSource

def launch_setup(context, *args, **kwargs):
    """
    Conditional launch setup based on hardware configuration
    """
    d455_arg = LaunchConfiguration('d455').perform(context)

    if d455_arg == 'true':
        # Real robot setup with RealSense D455
        print("🚀 Launching RTAB-Map with RealSense D455 camera...")
        return [
            IncludeLaunchDescription(
                PythonLaunchDescriptionSource([
                    PathJoinSubstitution([
                        get_package_share_directory('rtabmap_isaacsim_d455'),
                        'launch',
                        'real_robot',
                        'realsense_d455_stereo.launch.py'
                    ])
                ])
            )
        ]
    else:
        # Isaac Sim simulation setup
        print("🤖 Launching RTAB-Map with Isaac Sim simulation...")
        return [
            IncludeLaunchDescription(
                PythonLaunchDescriptionSource([
                    PathJoinSubstitution([
                        get_package_share_directory('rtabmap_isaacsim_d455'),
                        'launch',
                        'simulation',
                        'isaac_sim.launch.py'
                    ])
                ]),
                launch_arguments={
                    'rtabmap_viz': LaunchConfiguration('rtabmap_viz'),
                    'localization': LaunchConfiguration('localization'),
                    'vo': LaunchConfiguration('vo'),
                    'stereo': LaunchConfiguration('stereo'),
                    'image_width': LaunchConfiguration('image_width'),
                    'image_height': LaunchConfiguration('image_height')
                }.items()
            )
        ]

def generate_launch_description():
    """
    Generate launch description with all available arguments
    """
    return LaunchDescription([
        # === HARDWARE SELECTION ===
        DeclareLaunchArgument(
            'd455', 
            default_value='false',
            choices=['true', 'false'], 
            description='Hardware selection: true=RealSense D455, false=Isaac Sim'
        ),
        
        # === SIMULATION PARAMETERS (only used when d455=false) ===
        DeclareLaunchArgument(
            'rtabmap_viz', 
            default_value='true',
            choices=['true', 'false'], 
            description='Launch RTAB-Map visualization'
        ),
        DeclareLaunchArgument(
            'localization', 
            default_value='false',
            choices=['true', 'false'], 
            description='Start in localization mode (requires existing map)'
        ),
        DeclareLaunchArgument(
            'vo', 
            default_value='none',
            choices=['none', 'rtabmap', 'isaac'], 
            description='Visual odometry: none, rtabmap, or isaac'
        ),
        DeclareLaunchArgument(
            'stereo', 
            default_value='true',
            choices=['true', 'false'], 
            description='Use stereo camera mode'
        ),
        DeclareLaunchArgument(
            'image_width', 
            default_value='960',
            description='Simulation image width (pixels)'
        ),
        DeclareLaunchArgument(
            'image_height', 
            default_value='600',
            description='Simulation image height (pixels)'
        ),

        # Launch conditional setup
        OpaqueFunction(function=launch_setup)
    ])

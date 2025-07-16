from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription, OpaqueFunction
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution
from ament_index_python.packages import get_package_share_directory
from launch.launch_description_sources import PythonLaunchDescriptionSource

def launch_setup(context, *args, **kwargs):
    
    d455_arg = LaunchConfiguration('d455').perform(context)

    if d455_arg == 'true':
        # Launch real robot setup
        return [
            IncludeLaunchDescription(
                PythonLaunchDescriptionSource([
                    PathJoinSubstitution([
                        get_package_share_directory('rtabmap_isaacsim_d455'),
                        'launch',
                        'realsense_d455_stereo.launch.py'
                    ])
                ])
            )
        ]
    else:
        # Launch simulation setup
        return [
            IncludeLaunchDescription(
                PythonLaunchDescriptionSource([
                    PathJoinSubstitution([
                        get_package_share_directory('rtabmap_isaacsim_d455'),
                        'launch',
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
    return LaunchDescription([
        DeclareLaunchArgument('d455', default_value='false',
                          choices=['true', 'false'], 
                          description='Use D455 camera instead of Isaac Sim.'),
        
        # Arguments for simulation mode
        DeclareLaunchArgument('rtabmap_viz', default_value='true',
                          choices=['true', 'false'], description='Start rtabmap_viz.'),
        DeclareLaunchArgument('localization', default_value='false',
                          choices=['true', 'false'], description='Start rtabmap in localization mode.'),
        DeclareLaunchArgument('vo', default_value='none',
                          choices=['none', 'rtabmap', 'isaac'], description='Enable visual odometry approach.'),
        DeclareLaunchArgument('stereo', default_value='true',
                          choices=['true', 'false'], description='Use stereo images.'),
        DeclareLaunchArgument('image_width', default_value='960',
                          description='Resize input images (simulation).'),
        DeclareLaunchArgument('image_height', default_value='600',
                          description='Resize input images (simulation).'),

        OpaqueFunction(function=launch_setup)
    ])

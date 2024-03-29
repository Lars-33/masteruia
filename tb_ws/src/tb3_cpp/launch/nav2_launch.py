import os

from ament_index_python import get_package_share_directory

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch_ros.actions import Node
#from launch.substitutions import PathJoinSubstitution, LaunchConfiguration, Command, FindExecutable 
from launch_ros.substitutions import FindPackageShare
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import SetRemap
from launch.actions import GroupAction
from launch_ros.actions import PushRosNamespace
from launch.substitutions import LaunchConfiguration
from launch.substitutions import TextSubstitution
import time

def generate_launch_description():


    # ros2 launch nav2_bringup localization_launch.py 
    
    localization=GroupAction(
        actions=[
            PushRosNamespace('tb'),
            IncludeLaunchDescription( 
                PythonLaunchDescriptionSource(
                    os.path.join(
                        get_package_share_directory('nav2_bringup'),
                        'launch/localization_launch.py'
                    )
                ),    
                launch_arguments={
                    'namespace':'tb',
                    'map':'map/Masterlabben.yaml',
                    'params_file':'src/tb3_cpp/params/nav2_param.yaml',
                    'use_sim_time':'false'
                }.items()
            )
        ]
    )

    navigation=GroupAction(
        actions=[
            PushRosNamespace('tb'),
            IncludeLaunchDescription( 
                PythonLaunchDescriptionSource(
                    os.path.join(
                        get_package_share_directory('nav2_bringup'),
                        'launch/navigation_launch.py'
                    )
                ),    
                launch_arguments={
                    #'map':'map/Masterlabben.yaml',
                    'params_file':'src/tb3_cpp/params/nav2_param.yaml',
                    'namespace':'tb',
                    'use_namespace':'true',
                    'use_sim_time':'false'
                        
                }.items()
            )
        ]
    )

    ld = LaunchDescription()

    #ld.add_action(navigation)
    ld.add_action(localization)
    return ld
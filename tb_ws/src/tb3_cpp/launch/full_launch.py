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


os.environ["TURTLEBOT3_MODEL"] = "waffle"

os.system('sudo chmod a+rw /dev/ttyACM0')
os.system('sudo chmod 666 /dev/ttyUSB0')

ARGUMENTS = [
    DeclareLaunchArgument('serial_port', default_value="/dev/ttyUSB1",
                          description='Serial port to connect to the husky.'),
]

def generate_launch_description():

    tb_spawn= GroupAction(
        actions=[
            PushRosNamespace('tb'),
            IncludeLaunchDescription(
                PythonLaunchDescriptionSource(
                    os.path.join(
                        get_package_share_directory('turtlebot3_bringup'),
                        'launch/robot.launch.py'
                    )
                ),
                        
                launch_arguments={
                    'tb3_param_dir':'./src/tb3_cpp/params/tb3_param.yaml'
                    #'__ns':'/tb'    
                    }.items()
            ),
        ]
    ),


        #  ros2 launch slam_toolbox online_async_launch.py 
    slam=GroupAction(
        actions=[
            PushRosNamespace('tb'),
            IncludeLaunchDescription(
                PythonLaunchDescriptionSource(
                    os.path.join(
                        get_package_share_directory('slam_toolbox'),
                        'launch/online_async_launch.py'
                    )
                ),
                launch_arguments={
                #'map':'/home/lars/MasterUiA/tb_ws/map/Masterlabben.yaml'
                'params_file':'src/tb3_cpp/params/mapper_params_lifelong.yaml'
                }.items()
            ),
        ]
    ),


        # ros2 launch nav2_bringup localization_launch.py 
    nav2=GroupAction(
        actions=[
            PushRosNamespace('tb'),
            IncludeLaunchDescription( 
                PythonLaunchDescriptionSource(
                    os.path.join(
                        get_package_share_directory('nav2_bringup'),
                        'launch/bringup_launch.py'
                    )
                ),    
                launch_arguments={
                    #'map':'map/Masterlabben.yaml'
                    'params_file':'src/tb3_cpp/params/nav2_param.yaml'
                        
                }.items()
            )
        ]
    )

        # ros2 launch nav2_bringup rviz_launch.py 
        #IncludeLaunchDescription(
        #    
        #    PythonLaunchDescriptionSource(
        #        os.path.join(
        #            get_package_share_directory('nav2_bringup'),
        #            'launch/rviz_launch.py'
        #        )
        #    ),
        #)

    ld = LaunchDescription(ARGUMENTS)
    ld.add_action(tb_spawn)
    ld.add_action(slam)
    ld.add_action(nav2)
    return ld


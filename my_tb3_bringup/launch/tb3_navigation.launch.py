from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, ExecuteProcess, IncludeLaunchDescription, RegisterEventHandler
from launch.event_handlers import OnProcessExit
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node

from ament_index_python.packages import get_package_share_directory

import os


def generate_launch_description():
    """Launch Gazebo, the TurtleBot3 robot model, Nav2, and RViz for localization/navigation."""

    gazebo_share = get_package_share_directory('turtlebot3_gazebo')
    nav2_share = get_package_share_directory('nav2_bringup')
    bringup_share = get_package_share_directory('my_tb3_bringup')

    # Keep the same headless Gazebo setup used for mapping.
    world_path = os.path.join(gazebo_share, 'worlds', 'turtlebot3_house.world')

    map_default = os.path.expanduser('~/house_map.yaml')

    map_yaml_path = LaunchConfiguration('map')

    use_sim_time = LaunchConfiguration('use_sim_time')

    tb3_nav2_share = get_package_share_directory('turtlebot3_navigation2')

    params_file = os.path.join(tb3_nav2_share,'param','burger.yaml')

    declare_map_arg = DeclareLaunchArgument(
        'map',
        default_value=map_default,
        description='Absolute path to the saved map YAML file for Nav2'
    )

    declare_use_sim_time_arg = DeclareLaunchArgument(
        'use_sim_time',
        default_value='True',
        description='Use simulated time for Gazebo and Nav2'
    )

    gzserver = ExecuteProcess(
        cmd=[
            'gzserver',
            world_path,
            '-s', 'libgazebo_ros_init.so',
            '-s', 'libgazebo_ros_factory.so'
        ],
        additional_env={
            'GAZEBO_MODEL_PATH':
            gazebo_share + ':' +
            os.path.join(gazebo_share, 'models')
        },
        output='screen'
    )

    robot_state_publisher = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(gazebo_share, 'launch', 'robot_state_publisher.launch.py')
        )
    )

    model_path = os.path.join(
        gazebo_share,
        'models',
        'turtlebot3_burger',
        'model.sdf'
    )

    spawn_robot = Node(
        package='gazebo_ros',
        executable='spawn_entity.py',
        name='spawn_entity',
        arguments=[
            '-entity', 'burger',
            '-file', model_path,
            '-x', '-1.6214754581451416',
            '-y', '3.7980031967163086',
            '-z', '0.0025725364685058594'
        ],
        parameters=[{'use_sim_time': use_sim_time}],
        output='screen'
    )

    nav2_bringup = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(nav2_share, 'launch', 'bringup_launch.py')
        ),
        launch_arguments={
            'use_sim_time': use_sim_time,
            'map': map_yaml_path,
            'slam': 'False',
            'autostart': 'True',
            'params_file': params_file
        }.items()
    )

    nav2_on_spawn_exit = RegisterEventHandler(
        event_handler=OnProcessExit(
            target_action=spawn_robot,
            on_exit=[nav2_bringup]
        )
    )

    '''rviz = Node(
        package='rviz2',
        executable='rviz2',
        name='rviz2',
        arguments=[
            '-d',
            os.path.join(bringup_share, 'rviz', 'nav2_default_view.rviz')
        ],
        parameters=[{'use_sim_time': True}],
        output='screen'
    )'''

    return LaunchDescription([
        declare_map_arg,
        declare_use_sim_time_arg,
        gzserver,
        robot_state_publisher,
        spawn_robot,
        nav2_on_spawn_exit
        # rviz
    ])

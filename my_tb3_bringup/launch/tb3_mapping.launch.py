from launch import LaunchDescription
from launch.actions import ExecuteProcess, IncludeLaunchDescription, RegisterEventHandler
from launch.event_handlers import OnProcessExit
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node

from ament_index_python.packages import get_package_share_directory

import os


def generate_launch_description():

    gazebo_share = get_package_share_directory('turtlebot3_gazebo')
    cartographer_share = get_package_share_directory('turtlebot3_cartographer')

    world_path = os.path.join(
        gazebo_share,
        'worlds',
        'turtlebot3_house.world'
    )

    # HEADLESS GAZEBO SERVER
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

    # ROBOT STATE PUBLISHER
    robot_state_publisher = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(gazebo_share, 'launch', 'robot_state_publisher.launch.py')
        )
    )

    # SPAWN ROBOT - Direct spawn_entity.py Node (actual process for OnProcessExit to monitor)
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
            '-x', '0.0',
            '-y', '0.0',
            '-z', '0.01'
        ],
        output='screen'
    )

    # CARTOGRAPHER SLAM - launches only after spawn_robot process exits successfully
    cartographer_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(
                cartographer_share,
                'launch',
                'cartographer.launch.py'
            )
        ),
        launch_arguments={
            'use_sim_time': 'True',
            'use_rviz': 'False'
        }.items()
    )

    # Event handler: trigger Cartographer only after spawn_entity.py process exits successfully
    cartographer_on_spawn_exit = RegisterEventHandler(
        event_handler=OnProcessExit(
            target_action=spawn_robot,
            on_exit=[cartographer_launch]
        )
    )

    # RVIZ - launches immediately (parallel with other components)
    rviz = Node(
        package='rviz2',
        executable='rviz2',
        output='screen'
    )

    return LaunchDescription([
        gzserver,
        robot_state_publisher,
        spawn_robot,
        cartographer_on_spawn_exit,
        rviz
    ])
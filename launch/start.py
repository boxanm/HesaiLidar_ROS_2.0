from launch import LaunchDescription
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory
from launch_ros.actions import ComposableNodeContainer
from launch_ros.descriptions import ComposableNode

def generate_launch_description():
    rviz_config=get_package_share_directory('hesai_ros_driver')+'/rviz/rviz2.rviz'
    ld = LaunchDescription([
        Node(namespace='rviz2', package='rviz2', executable='rviz2', arguments=['-d',rviz_config])
    ])
    ld.add_action(ComposableNodeContainer(
        name='lidar_pipeline',
        namespace='',
        package='rclcpp_components',
        executable='component_container_mt',
        output='screen',
        composable_node_descriptions=[
            ComposableNode(
                package='hesai_ros_driver',
                plugin='SourceDriver',
                name='hesai_ros_driver_node',
                extra_arguments=[{'use_intra_process_comms': True}],
            ),
            ComposableNode(
                package='utility_nodes',
                plugin='TopicHzNode',
                name='topic_hz_nde',
                parameters=[{'topic_name': '/lidar_points'}],
                extra_arguments=[{'use_intra_process_comms': True}],
            ),
            ComposableNode(
                package='tcp_tunnel',
                plugin='TCPTunnelServer',
                name='tcp_tunnel_server',
                extra_arguments=[{'use_intra_process_comms': True}],
            ),
        ]
    ))
    return ld

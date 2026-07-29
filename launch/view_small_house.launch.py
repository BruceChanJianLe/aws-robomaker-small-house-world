import os

from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from ament_index_python.packages import get_package_share_directory


def generate_launch_description():
    # View the small house in the modern gz GUI (server + client).
    # Requires a working display (the conda gz build renders via GLX/OGRE2).
    package_dir = get_package_share_directory('aws_robomaker_small_house_world')

    return LaunchDescription([
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(
                os.path.join(package_dir, 'launch', 'small_house.launch.py')
            ),
            launch_arguments={'gui': 'true'}.items(),
        )
    ])


if __name__ == '__main__':
    generate_launch_description()

# /*******************************************************************************
# * Copyright 2019 ROBOTIS CO., LTD.
# *
# * Licensed under the Apache License, Version 2.0 (the "License");
# * you may not use this file except in compliance with the License.
# * You may obtain a copy of the License at
# *
# *     http://www.apache.org/licenses/LICENSE-2.0
# *
# * Unless required by applicable law or agreed to in writing, software
# * distributed under the License is distributed on an "AS IS" BASIS,
# * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# * See the License for the specific language governing permissions and
# * limitations under the License.
# *******************************************************************************/

# /* Author: Darby Lim */
# Ported from Gazebo Classic (gazebo_ros gzserver/gzclient) to modern gz
# (Ignition, via ros_gz_sim). The gz system plugins live in the world file.

import os

from launch import LaunchDescription
from launch.actions import (
    DeclareLaunchArgument,
    IncludeLaunchDescription,
    AppendEnvironmentVariable,
)
from launch.substitutions import LaunchConfiguration, PythonExpression
from launch.launch_description_sources import PythonLaunchDescriptionSource
from ament_index_python.packages import get_package_share_directory


def generate_launch_description():
    package_dir = get_package_share_directory('aws_robomaker_small_house_world')
    gz_sim_share = get_package_share_directory('ros_gz_sim')

    world = LaunchConfiguration(
        'world', default=os.path.join(package_dir, 'worlds', 'small_house.world')
    )
    gui = LaunchConfiguration('gui', default='false')
    use_sim_time = LaunchConfiguration('use_sim_time', default='true')

    # gz sim: no '-s' => server + GUI; '-s' => headless server only. '-r' => start running.
    gz_sim = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(gz_sim_share, 'launch', 'gz_sim.launch.py')
        ),
        launch_arguments={
            'gz_args': PythonExpression(
                ["'", world, " -r' if '", gui, "' == 'true' else '", world, " -r -s'"]
            )
        }.items(),
    )

    return LaunchDescription([
        # so model:// references inside small_house.world resolve
        AppendEnvironmentVariable(
            name='GZ_SIM_RESOURCE_PATH', value=os.path.join(package_dir, 'models')
        ),
        AppendEnvironmentVariable(
            name='GZ_SIM_RESOURCE_PATH', value=os.path.join(package_dir, 'worlds')
        ),
        DeclareLaunchArgument(
            'world',
            default_value=os.path.join(package_dir, 'worlds', 'small_house.world'),
            description='SDF world file'),
        DeclareLaunchArgument(
            'gui',
            default_value='false',
            description='Run the gz GUI (true) or headless server only (false)'),
        DeclareLaunchArgument(
            'use_sim_time',
            default_value='true'),
        gz_sim,
    ])


if __name__ == '__main__':
    generate_launch_description()

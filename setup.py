import os
from glob import glob
from setuptools import find_packages, setup

package_name = 'ros2_golf_ball_feeder'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (os.path.join('share', package_name, 'launch'), glob('launch/*.launch.py')),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='amane',
    maintainer_email='amanegodo@gmail.com',
    description='TODO: Package description',
    license='TODO: License declaration',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': [
            'tee_sensor_node = ros2_golf_ball_feeder.tee_sensor_node:main',
            'feeder_supervisor_node = ros2_golf_ball_feeder.feeder_supervisor_node:main',
            'actuator_node = ros2_golf_ball_feeder.actuator_node:main',
        ],
    },
)

from setuptools import find_packages, setup
import os
from glob import glob

package_name = 'perception'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(include=['perception', 'perception.*']),
    data_files=[
        ('share/ament_index/resource_index/packages', ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (os.path.join('share', package_name, 'launch'), glob('launch/*.py')),
        (os.path.join('share', package_name, 'artifacts'), glob('src/perception/perception/artifacts/*')),
        (os.path.join('lib', package_name, 'artifacts'), glob('src/perception/perception/artifacts/*')),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='youssef',
    maintainer_email='yousefkamel282@gmail.com',
    description='ROS2 perception package for object tracking and motion estimation',
    license='Apache License 2.0',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'camera_stream = perception.camera_stream:main',
            'tracking = perception.tracking:main',
            'speed = perception.speed:main',
            'processor = perception.processor:main',
        ],
    },
)

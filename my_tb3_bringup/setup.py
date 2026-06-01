import os

from setuptools import find_packages, setup

package_name = 'my_tb3_bringup'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
    (
        'share/ament_index/resource_index/packages',
        ['resource/' + package_name],
    ),
    (
        'share/' + package_name,
        ['package.xml'],
    ),
    (
        os.path.join('share', package_name, 'launch'),
        ['launch/tb3_mapping.launch.py'],
    ),
    (
        os.path.join('share', package_name, 'launch'),
        ['launch/tb3_navigation.launch.py'],
    ),
],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='saket',
    maintainer_email='saketsalt@gmail.com',
    description='TODO: Package description',
    license='TODO: License declaration',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': [
            'room_navigator = my_tb3_bringup.room_navigator:main',
            'decision_node = my_tb3_bringup.decision_node:main',
            'input_node = my_tb3_bringup.input_node:main',
            'predict_room = my_tb3_bringup.predict_room:main',
        ],
    },
)

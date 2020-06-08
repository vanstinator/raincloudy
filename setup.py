# coding=utf-8
"""RainCloudy setup script."""
from setuptools import setup


def readme():
    with open('README.rst') as desc:
        return desc.read()


setup(
    name='raincloudy',
    packages=['raincloudy'],
    version='1.1.1',
    description='A Python library to communicate with Melnor \
                 RainCloud Smart Garden Watering Irrigation Timer \
                 (https://wwww.melnor.com/)',
    long_description=readme(),
    author='Marcelo Moreira de Mello',
    author_email='tchello.mello@gmail.com',
    url='https://github.com/tchellomello/raincloudy',
    license='Apache License 2.0',
    include_package_data=True,
    install_requires=[
        'requests>=2.0',
        'bs4',
        'urllib3>=1.22',
        'html5lib==1.0.1'
    ],
    test_suite='tests',
    keywords=[
        'garden',
        'irrigation',
        'melnor',
        'rain cloud',
        'water',
    ],
)

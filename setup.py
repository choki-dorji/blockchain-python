from setuptools import setup


setup(
    name='druk',
    version='0.1',
    packages=['druk'],
    install_requires=[
        'ecdsa',
        'pytest',
    ],
    entry_points={
        'console_scripts': ['druk=druk.main:main'],
    },
)

from os import path
from setuptools import setup, find_packages
from codecs import open

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='MindPong',
    version='0.1',

    description='MindPong is a fun game demonstrating neurotechnologies',
    long_description=long_description,
    url='https://github.com/PolyCortex/MindPong',
    author='PolyCortex',
    author_email='polycortex@gmail.com',
    license='MIT',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Application',
        'Programming Language :: Python :: 2.7',
    ],
    keywords='muse polycortex eeg concentration beta',
    packages=find_packages(exclude=['contrib', 'docs', 'tests']),


    install_requires=['pexpect', 'pyserial', 'numpy', 'pyMuse'],

    entry_points={
        'console_scripts': [
            'boatGUI=boatGUI:main',
        ],
    },
)

from os import path
import sys
from setuptools import setup, find_packages
from codecs import open
from platform import machine, system
from pip._internal import main as pip

if (system() != 'Windows'):
    sys.exit('Currently, the only supported OS for MindPong is Windows')

pyqt_link = ''
if machine() == 'AMD64':
    pyqt_link = 'https://download.lfd.uci.edu/pythonlibs/o4uhg4xd/PyQt4-4.11.4-cp27-cp27m-win_amd64.whl#egg=PyQt4'
elif machine() == 'x86':
    pyqt_link = 'https://download.lfd.uci.edu/pythonlibs/o4uhg4xd/PyQt4-4.11.4-cp27-cp27m-win32.whl#egg=PyQt4'
else:
    sys.exit('Your architecture is not compatible with any version of PyQt4. Sorry :(')

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

try:
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


        install_requires=['pexpect', 'pyserial', 'numpy', 'wheel', 'pyMuse'],
        dependency_links=[
            'https://github.com/PolyCortex/pyMuse/archive/ExtractMindPongApp.zip#egg=pyMuse',
            'https://files.pythonhosted.org/packages/f7/f3/90837bee8673a1bc658ed908601a8e35290acec297b0f487d1a59d08e5b1/numpy-1.15.1-cp27-none-win_amd64.whl'
        ],

        entry_points={
            'console_scripts': [
                'boatGUI=boatGUI:main',
            ],
        },
    )
    pip(['install', pyqt_link])
    print('\nINSTALLATION COMPLETED!')
except:
    print "Unexpected error:", sys.exc_info()[0]
    raise

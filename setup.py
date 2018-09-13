import sys
from setuptools import setup, find_packages
from setuptools.command.build_ext import build_ext as _build_ext
from codecs import open
from os import path
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

class build_ext(_build_ext):
    'to install numpy'
    def finalize_options(self):
        _build_ext.finalize_options(self)
        # Prevent numpy from thinking it is still in its setup process:
        __builtins__.__NUMPY_SETUP__ = False
        print('This might take a while (approx 4-5 minutes). Do not exit')
        import numpy
        self.include_dirs.append(numpy.get_include())

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

        cmdclass={ 'build_txt': build_ext },
        setup_requires=['numpy'],

        install_requires=['pexpect', 'pyserial', 'numpy', 'wheel', 'pyMuse'],
        dependency_links=['https://github.com/PolyCortex/pyMuse/archive/ExtractMindPongApp.zip#egg=pyMuse'],
        
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


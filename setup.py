# Always prefer setuptools over distutils
from setuptools import setup
# To use a consistent encoding
from codecs import open
from os import path
import meta

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='callgr',
    version=meta.__version__,
    description=meta.__description__,
    long_description=long_description,
    url=meta.__url__,
    author=meta.__author__,
    author_email=meta.__email__,
    license='MIT',
    py_modules=['callgr', 'meta'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: MIT License',
        'Programming Language :: Python :: 2.x',
    ],

    entry_points={
        'console_scripts': [
            'callgr=callgr:main',
        ],
    },
)

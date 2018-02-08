#!/usr/bin/env python

# References:
# https://github.com/pypa/sampleproject
# https://github.com/j0057/setuptools-version-command
# http://www.plope.com/Members/chrism/nose_setup_py_test

ez_setup.use_setuptools()

from setuptools import setup, find_packages  # Always prefer setuptools over distutils
from codecs import open  # To use a consistent encoding
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the relevant file
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='selcald',

    # Versions should comply with PEP440.  For a discussion on single-sourcing
    # the version across setup.py and the project code, see
    # https://packaging.python.org/en/latest/single_source_version.html
    version_command=( 'git describe', 'pep440-git-local' ),

    description="Selective calling (SELCAL) decoder",
    long_description=long_description,

    # The project's main homepage.
    url="https://bitbucket.org/techn0mad/selcald",
    download_url="https://bitbucket.org/techn0mad/selcald/get/59271168797a.zip",

    # Author details
    author="Larry Gadallah",
    author_email="lgadallah@gmail.com",

    # Choose your license
    license="LGPL",

    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 2 - Pre-Alpha',

        # Indicate who your project is intended for
        'Intended Audience :: Developers',
        'Topic :: Communications :: Ham Radio',
        'Topic :: Multimedia :: Sound/Audio :: Analysis',

        # Pick your license as you wish (should match "license" above)
        'License :: OSI Approved :: GNU Library or Lesser General Public License (LGPL)',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        'Programming Language :: Python :: 2.7',
    ],

    # What does your project relate to?
    keywords = 'dsp signal processing radio aviation',

    # You can just specify the packages manually here if your project is
    # simple. Or you can use find_packages().
    packages = find_packages(exclude=['contrib', 'docs', 'tests*']),

    # List run-time dependencies here.  These will be installed by pip when your
    # project is installed. For an analysis of "install_requires" vs pip's
    # requirements files see:
    # https://packaging.python.org/en/latest/requirements.html
    install_requires = [ 'numpy', 'scipy', ],

    # List additional groups of dependencies here (e.g. development dependencies).
    # You can install these using the following syntax, for example:
    # $ pip install -e .[dev,test]
    extras_require = {
        'dev': ['check-manifest', 'setuptools-version-command', 'setuptools-lint', 'pylint', 'sphinx', 'numpy', 'scipy', ],
        'test': ['coverage', 'nose', 'nose-parameterized', 'nosexcover', 'nose-testconfig', 'mock', ],
    },

    # A string or list of strings specifying what other distributions need to
    # be present in order for the setup script to run. setuptools will attempt
    # to obtain these (even going so far as to download them using EasyInstall)
    # before processing the rest of the setup script or commands. This argument
    # is needed if you are using distutils extensions as part of your build
    # process; for example, extensions that process setup() arguments and turn
    # them into EGG-INFO metadata files.
    #
    # (Note: projects listed in setup_requires will NOT be automatically
    # installed on the system where the setup script is being run. They are simply
    # downloaded to the ./.eggs directory if they're not locally available already.
    # If you want them to be installed, as well as being available when the setup
    # script is run, you should add them to install_requires and setup_requires.)
    setup_requires = { 'setuptools-version-command', 'setuptools-lint', 'pylint', 'sphinx', 'coverage', 'nose',
                       'nose-parameterized', 'nosexcover', 'mock', },

    test_suite = 'nose.collector',
    tests_require = [ 'coverage', 'nose', 'nose-parameterized', 'nosexcover', 'nose-testconfig', 'mock', ],

    # If there are data files included in your packages that need to be
    # installed, specify them here.  If using Python 2.6 or less, then these
    # have to be included in MANIFEST.in as well.
    package_data = {
        'selcald': [],
    },

    # Although 'package_data' is the preferred approach, in some case you may
    # need to place data files outside of your packages.
    # see http://docs.python.org/3.4/distutils/setupscript.html#installing-additional-files
    # In this case, 'data_file' will be installed into '<sys.prefix>/my_data'
    # data_files=[('my_data', ['data/data_file'])],

    # To provide executable scripts, use entry points in preference to the
    # "scripts" keyword. Entry points provide cross-platform support and allow
    # pip to create the appropriate form of executable for the target platform.
    # entry_points={
    #    'console_scripts': [
    #        'sample=sample:main',
    #    ],
    #},

    # Scripts are files containing Python source code, intended to be started
    # from the command line. Scripts don't require Distutils to do anything
    # very complicated. The only clever feature is that if the first line of
    # the script starts with #! and contains the word "python", the Distutils
    # will adjust the first line to refer to the current interpreter location.
    # By default, it is replaced with the current interpreter location. The
    # --executable (or -e) option will allow the interpreter path to be
    # explicitly overridden.
    #
    # The scripts option simply is a list of files to be handled in this way.
    scripts = [],
)

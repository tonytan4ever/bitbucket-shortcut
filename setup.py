#!/usr/bin/env python
from __future__ import print_function
try:
    from setuptools import setup, find_packages
except ImportError:
    from ez_setup import use_setuptools
    use_setuptools()
    from setuptools import setup, find_packages


install_requires = ['requests', 'GitPython']

setup(
    name="BitbucketShortcuts",
    version=VERSION,
    description="Python Git Library",
    author="Tony Tan",
    author_email="tonytan198211@gmail.com",
    url="https://github.com/tonytan4ever",
    packages=find_packages('.'),
    license="MIT License",
    install_requires=install_requires,
    test_requirements=test_requires + install_requires,
    zip_safe=False,
    long_description="""BitbucketShortcuts provides command line utilities for Bitbucket operations""",
    classifiers=[
        # Picked from
        #   http://pypi.python.org/pypi?:action=list_classifiers
        # "Development Status :: 1 - Planning",
        # "Development Status :: 2 - Pre-Alpha",
        # "Development Status :: 3 - Alpha",
        # "Development Status :: 4 - Beta",
        "Development Status :: 5 - Production/Stable",
        # "Development Status :: 6 - Mature",
        # "Development Status :: 7 - Inactive",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Operating System :: POSIX",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: MacOS :: MacOS X",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
    ]
)
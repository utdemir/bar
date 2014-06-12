#!/usr/bin/env python

from distutils.core import setup

setup(name='pbar',
      version='0.1.0',
      description='Configurable progress bars/status monitors for Python console applications.',
      url='https://github.com/utdemir/pbar',
      author='Utku Demir',
      author_email='utdemir@gmail.com',
      py_modules=['pbar'],
      classifiers=[
          'Environment :: Other Environment',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: GNU General Public License (GPL)',
          'Operating System :: POSIX',
          'Programming Language :: Python :: 2',
          'Programming Language :: Python :: 3',
          'Topic :: Software Development :: Libraries :: Python Modules'
          ],
      )
#!/usr/bin/env python

from distutils.core import setup

setup(name='bar',
      version='0.2.0',
      description='Configurable progress bars/status monitors for Python console applications.',
      url='https://github.com/utdemir/bar',
      author='Utku Demir',
      author_email='utdemir@gmail.com',
      py_modules=['bar'],
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

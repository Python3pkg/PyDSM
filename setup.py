#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (c) 2014, Sergio Callegari
# All rights reserved.

# This file is part of PyDSM.

# PyDSM is free software: you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# PyDSM is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with PyDSM.  If not, see <http://www.gnu.org/licenses/>.

import sys
from distutils.core import setup
from distutils.core import Command
from distutils import ccompiler
from distutils.extension import Extension
from Cython.Build import cythonize
import platform
import numpy


# Find version
__version__=''
execfile('pydsm/_version.py')


class test (Command):
    description = "Test the pydsm distribution prior to install"

    user_options = [
        ('test-file=', None,
         'Testfile to run in the test directory'),
        ]

    def initialize_options (self):
        self.build_base = 'build'
        self.test_dir = 'test'
        self.test_file = 'test_all'

    def finalize_options (self):
        build = self.get_finalized_command('build')
        self.build_purelib = build.build_purelib
        self.build_platlib = build.build_platlib

    def run (self):
        # Invoke the 'build' command
        self.run_command ('build')
        # remember old sys.path to restore it afterwards
        old_path = sys.path[:]
        # extend sys.path
        sys.path.insert(0, self.build_purelib)
        sys.path.insert(0, self.build_platlib)
        sys.path.insert(0, self.test_dir)
        # build include path for test
        TEST=__import__(self.test_file)
        suite = TEST.unittest.TestLoader().loadTestsFromModule(TEST)
        TEST.unittest.TextTestRunner(verbosity=2).run(suite)
        sys.path = old_path[:]


# We want the default compiler to be mingw32 in windows
ccompiler._default_compilers=\
        (('nt', 'mingw32'),)+ccompiler._default_compilers

# Prepare the extension modules
ext_modules=[
    Extension('pydsm.delsig._simulateDSM_cblas',
              ['pydsm/delsig/_simulateDSM_cblas.pyx']),
    Extension('pydsm.delsig._simulateDSM_scipy_blas',
              ['pydsm/delsig/_simulateDSM_scipy_blas.pyx'])]

description=u'Python Based ΔΣ modulator design tools'
long_description=u"""
Python Based ΔΣ modulator design tools.

Based on the algorithms in Callegari, Bizzarri 'Output Filter Aware
Optimization of the Noise Shaping Properties of ΔΣ Modulators via
Semi-Definite Programming', IEEE Transactions on Circuits and Systems I,
2013 and others.

Portion of code ported to python from the DELSIG toolbox by R. Schreier.
"""

# Fix stuff for Windows
if platform.system()=='Windows':
    ext_modules=[
        Extension('pydsm.delsig._simulateDSM_scipy_blas',
                  ['pydsm/delsig/_simulateDSM_scipy_blas.pyx'],
                  define_macros=[('__USE_MINGW_ANSI_STDIO','1')],
                  include_dirs=[numpy.get_include()])]
    description='Python Based Delta-Sigma modulator design tools'
    long_description="""
Python Based Delta-Sigma modulator design tools.

Based on the algorithms in Callegari, Bizzarri 'Output Filter Aware
Optimization of the Noise Shaping Properties of Delta-Sigma Modulators via
Semi-Definite Programming', IEEE Transactions on Circuits and Systems I,
2013 and others.

Portion of code ported to python from the DELSIG toolbox by R. Schreier.
"""


setup(name='pydsm',
      version=__version__,
      description=description,
      author='Sergio Callegari',
      author_email='sergio.callegari@unibo.it',
      url='http://pydsm.googlecode.com',
      packages = ['pydsm', 'pydsm.simulation', 'pydsm.NTFdesign',
                  'pydsm.NTFdesign.filter_based', 'pydsm.delsig',
                  'pydsm.NTFdesign.weighting'],
      ext_modules=cythonize(ext_modules),
      requires=['scipy(>=0.10.1)',
                'numpy(>=1.6.1)',
                'matplotlib(>= 1.1.0)',
                'cvxopt(>=1.1.4)',
                'cython(>=0.16)'],
      cmdclass = {'test': test},
      license = 'Simplified BSD License',
      platforms = ['Linux','Windows','Mac'],
      long_description = long_description)

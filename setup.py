# Copyright 2016 ELIFE. All rights reserved.
# Use of this source code is governed by a MIT
# license that can be found in the LICENSE file.

from distutils.core import setup, Extension


with open('docs/README.rst') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='chemevolve',
    version='0.0.2',
    description='Tools for Simulating Chemical Evoltion',
    long_description=readme,
    maintainer='Cole Mathis',
    maintainer_email='cole.mathis@asu.edu',
    url='https://github.com/elife-asu/chemevolve',
    license=license,
    requires=['numpy', 'matplotlib', 'seaborn'],
    # packages=[],
    # package_data = { },
    # test_suite = "test",
    #platforms = ["Windows", "OS X", "Linux"]
)





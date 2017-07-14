# Copyright 2016 ELIFE. All rights reserved.
# Use of this source code is governed by a MIT
# license that can be found in the LICENSE file.
from setuptools import setup,find_packages


with open('docs/README.rst') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='chemevolve',
    version='0.0.8',
    description='Tools for Simulating Chemical Evoltion',
    long_description=readme,
    maintainer='Cole Mathis',
    maintainer_email='cole.mathis@asu.edu',
    url='https://github.com/elife-asu/chemevolve',
    license=license,
    install_requires=['numpy', 'matplotlib', 'seaborn'],
    packages=find_packages(),
    include_package_data = True
   
)





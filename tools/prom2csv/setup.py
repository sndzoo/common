#  Copyright (c) 2019 Manuel Peuster, Paderborn University
# ALL RIGHTS RESERVED.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# Neither the name of Paderborn University
# nor the names of its contributors may be used to endorse or promote
# products derived from this software without specific prior written
# permission.
#
# This work has also been performed in the framework of the 5GTANGO project,
# funded by the European Commission under Grant number 761493 through
# the Horizon 2020 and 5G-PPP programmes. The authors would like to
# acknowledge the contributions of their colleagues of the SONATA
# partner consortium (www.5gtango.eu).

from setuptools import setup, find_packages


setup(name='prom2csv',
      license='Apache License, Version 2.0',
      version='0.1',
      url='sndzoo.github.io',
      author='Manuel Peuster',
      author_email='manuel@peuster.de',
      long_description="Export Prometheus metrics to CSV files.",
      packages=find_packages(exclude=['docs']),
      package_data={  # Optional
        'prom2csv': ['metrics.yml'],
      },
      include_package_data=True,
      python_requires=">=3.5",
      install_requires=[
          "argparse",
          "pyaml",
          "requests",
          "pandas"
      ],
      zip_safe=False,
      entry_points={
          'console_scripts': [
              'prom2csv=prom2csv:main'
          ],
      },
      test_suite='prom2csv',
      setup_requires=[],
      tests_require=['pytest'])

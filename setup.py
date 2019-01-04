#!/usr/bin/env python
#
# Copyright 2019 leenjewel
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

try :
    import setuptools
    from setuptools import setup
except ImportError :
    setuptools = None
    from distutils.core import setup

kwargs = {}

version = "1.0.0"

setup(
    name = "pykcp",
    version = version,
    packages = ["pykcp"],
    package_data = {},
    author = "leenjewel",
    author_email = "leenjewel@gmail.com",
    url="https://github.com/leenjewel/pykcp",
    license="http://www.apache.org/licenses/LICENSE-2.0",
    description="PyKCP is a KCP protocol by python",
    install_requires=["tornado"]
    **kwargs
)


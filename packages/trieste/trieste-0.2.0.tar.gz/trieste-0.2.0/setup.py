# Copyright 2020 The Trieste Contributors
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

from setuptools import find_packages, setup

with open("README.md", "r") as file:
    long_description = file.read()

setup(
    name="trieste",
    version="0.2.0",
    author="The Trieste contributors",
    author_email="labs@secondmind.ai",
    description="A Bayesian optimization research toolbox built on TensorFlow",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/secondmind-labs/trieste",
    packages=find_packages(include=("trieste*",)),
    classifiers=[
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    python_requires="~=3.7",
    install_requires=[
        "absl-py",
        "gpflow==2.1.*",
        "numpy",
        "tensorflow>=2.1,!=2.2.0,!=2.3.0",  # !=2.2.0,!=2.3.0 because of https://github.com/advisories/GHSA-8fxw-76px-3rxv
        "tensorflow-probability>=0.9",
    ],
)

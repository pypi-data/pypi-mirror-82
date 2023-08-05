# This file is part of spectralLib.
#
# Copyright 2020, Tom George Ampiath, All rights reserved.
#
# spectralLib is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# spectralLib is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with spectralLib.  If not, see <http://www.gnu.org/licenses/>.

import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

long_description += """

"""

with open("CHANGELOG.md", "r") as fh:
    long_description += fh.read()

setuptools.setup(
    name="spectralLib",
    version="0.0.3",
    author="Tom George Ampiath",
    author_email="itomgeorgeampiath@gmail.com",
    description="A python library for analyzing multi and hyper spectral images.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/TomAmpiath/spectralLib",
    packages=setuptools.find_packages(),
    install_requires=["numpy", "matplotlib", "scipy", "vtk"],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Science/Research",
        "Natural Language :: English",
        "Topic :: Scientific/Engineering",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    keywords="spectralUI hyperspectral multispectral PySide2 Qt spectralLib",
)

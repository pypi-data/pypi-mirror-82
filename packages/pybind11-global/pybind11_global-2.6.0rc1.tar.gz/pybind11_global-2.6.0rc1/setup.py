#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Setup script for pybind11-global (in the sdist or in tools/setup_global.py in the repository)
# This package is targeted for easy use from CMake.

import contextlib
import glob
import os
import re
import shutil
import subprocess
import sys
import tempfile

# Setuptools has to be before distutils
from setuptools import setup

from distutils.command.install_headers import install_headers

class InstallHeadersNested(install_headers):
    def run(self):
        headers = self.distribution.headers or []
        for header in headers:
            # Remove pybind11/include/
            short_header = header.split("/", 2)[-1]

            dst = os.path.join(self.install_dir, os.path.dirname(short_header))
            self.mkpath(dst)
            (out, _) = self.copy_file(header, dst)
            self.outfiles.append(out)


main_headers = glob.glob("pybind11/include/pybind11/*.h")
detail_headers = glob.glob("pybind11/include/pybind11/detail/*.h")
cmake_files = glob.glob("pybind11/share/cmake/pybind11/*.cmake")
headers = main_headers + detail_headers

cmdclass = {"install_headers": InstallHeadersNested}


# This will _not_ affect installing from wheels,
# only building wheels or installing from SDist.
# Primarily intended on Windows, where this is sometimes
# customized (for example, conda-forge uses Library/)
base = os.environ.get("PYBIND11_GLOBAL_PREFIX", "")

# Must have a separator
if base and not base.endswith("/"):
    base += "/"

setup(
    name="pybind11_global",
    version="2.6.0rc1",
    packages=[],
    headers=headers,
    data_files=[
        (base + "share/cmake/pybind11", cmake_files),
        (base + "include/pybind11", main_headers),
        (base + "include/pybind11/detail", detail_headers),
    ],
    cmdclass=cmdclass,
)

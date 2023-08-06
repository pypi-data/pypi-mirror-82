# -*- coding: utf-8 -*-
# Copyright (C) Cardiff University (2019-2020)
#
# This file is part of ciecplib
#
# ciecplib is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# ciecplib is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with ciecplib.  If not, see <http://www.gnu.org/licenses/>.

"""Build configuration for ciecplib
"""

import re
from pathlib import Path

from setuptools import (find_packages, setup)
from setuptools.command.build_py import build_py
from setuptools.command.install import install

try:
    from build_manpages.build_manpages import (
        build_manpages,
        get_build_py_cmd,
        get_install_cmd,
    )
except ImportError:  # can't build manpages, that's ok
    cmdclass = {
        "build_py": build_py,
        "install": install,
    }
else:
    cmdclass = {
        "build_manpages": build_manpages,
        "build_py": get_build_py_cmd(build_py),
        "install": get_install_cmd(install),
    }

__author__ = "Duncan Macleod <duncan.macleod@ligo.org>"


def find_version(path, varname="__version__"):
    """Parse the version metadata in the given file.
    """
    with path.open('r') as fobj:
        version_file = fobj.read()
    version_match = re.search(
        r"^{0} = ['\"]([^'\"]*)['\"]".format(varname),
        version_file,
        re.M,
    )
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")


setup_requires = [
    "setuptools",  # MIT
]
install_requires = [
    "M2Crypto",  # MIT
    "pyOpenSSL",  # Apache-2.0
    "requests",  # Apache-2.0
    "requests-ecp",  # GPL-3.0-or-later
]
tests_require = [
    "pytest >= 3.9.0",
    "pytest-cov",
    "requests-mock",
]
extras_require = {
    "test": tests_require,
    "docs": [
        "sphinx",
        "sphinx-argparse",
        "sphinx_automodapi",
        "sphinx_rtd_theme",
        "sphinx_tabs",
    ],
}

setup(
    # distribution metadata
    name="ciecplib",
    version=find_version(Path("ciecplib") / "__init__.py"),
    author="Duncan Macleod",
    author_email="duncan.macleod@ligo.org",
    license="GPL-3.0-or-later",
    description="A python client for SAML ECP authentication",
    long_description=open("README.md", "r").read(),
    long_description_content_type="text/markdown",
    url="https://pypi.org/project/ciecplib/",
    project_urls={
        "Bug Tracker": "https://github.com/duncanmmacleod/ciecplib/issues",
        "Documentation": "https://ciecplib.readthedocs.io/",
        "Source Code": "https://github.com/duncanmmacleod/ciecplib/",
    },
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Topic :: Scientific/Engineering',
    ],
    # contents
    packages=find_packages(),
    entry_points={
        "console_scripts": [
            "ecp-cert-info=ciecplib.tool.ecp_cert_info:main",
            "ecp-curl=ciecplib.tool.ecp_curl:main",
            "ecp-get-cert=ciecplib.tool.ecp_get_cert:main",
            "ecp-get-cookie=ciecplib.tool.ecp_get_cookie:main",
        ],
    },
    # dependencies
    cmdclass=cmdclass,
    python_requires=">=3.5",
    setup_requires=setup_requires,
    install_requires=install_requires,
    tests_require=tests_require,
    extras_require=extras_require,
)

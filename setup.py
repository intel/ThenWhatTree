# Copyright (C) 2018 Intel Corporation
# SPDX-License-Identifier: BSD-3-Clause

from setuptools import setup, Extension, find_packages
import sys

setup(name='ThenWhatTree',
      version='1.0',
      description='',
      author='Erik Berg',
      author_email='',
      url='',
      packages=find_packages(),
      install_requires=['python_magic', 'pathlib'],
      entry_points={'console_scripts': [
            'create_lib = ThenWhatTree.create_nodes_for_xml_elements:main',
            'execute = ThenWhatTree.execute_tree:main',
      ],
      },
      requires=['python_magic', 'pathlib'],
      python_requires=">=3.6.1",
      )

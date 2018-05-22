

# Copyright (C) 2018 Intel Corporation
# SPDX-License-Identifier: BSD-3-Clause

""" Create decision tree modules and documentation

Functions available in this module:
xml_to_tree()
text_to_xml()

"""

# Import built in modules
import os
from shutil import copyfile, SameFileError
# noinspection PyPep8Naming
from xml.etree import ElementTree

# Import 3rd party modules
import magic as magic

from ThenWhatTree.lib.twt_node.create_node import create_node

# Import local modules

# Module authorship metadata
__author__ = "Erik W Berg"
__copyright__ = "Copyright 2018, Intel Corporation"
__credits__ = [""]
__license__ = "BSD-3-Clause"
__version__ = "1.0"
__maintainer__ = "Erik W Berg"
__email__ = ""
__status__ = "Production"  # Prototype, Development, Production


# Code starts here


def xml_to_tree(xml_file, lib_path):
    """
    Generate all decision tree nodes in an XML file and write then to the lib_path/lib_name directory

    :param xml_file: full path to the XML file
    :param lib_path: full path to the library where all nodes will be created
    :return:
    """

    tree_object = _create_tree_object_from_xml(xml_file)
    _create_tree(lib_path, tree_object)
    _write_file_to_directory(xml_file, lib_path)


##################################################################################

def _create_tree_object_from_xml(xml_file):
    """

    :param xml_file: full path to the XML file
    :return: ElementTree instance for the xml_file
    """

    return ElementTree.parse(xml_file)


def _write_file_to_directory(xml_file, lib_path):
    """

    :param xml_file: full path to the xml file
    :param lib_path: full path to the directory where the xml and decision tree node modules will be written
    :return: None
    """
    xml_file_name = os.path.basename(xml_file)
    try:
        copyfile(xml_file, os.path.join(lib_path, xml_file_name))
    except SameFileError:
        pass


def _create_tree(lib_path, tree_object):
    """
    Iterate through the elements in the tree_object and create a node module for each one.

    :param lib_path: full path to the library where all nodes will be created
    :param tree_object: ElementTree instance for the xml_file
    :return: None
    """
    for element in tree_object.iter('node'):
        create_node(lib_path, element)


def get_tree_root_element(tree_object):
    """
    Return the root of the tree_object

    :param tree_object: ElementTree instance for the xml_file
    :return: Root object of the ElementTree instance
    """
    return tree_object.getroot()


def create_tree_object_from_xml(xml_file):
    """

    :param xml_file:
    :return: root element of ElementTree created from xml_file
    """
    return ElementTree.parse(xml_file)


def _get_file_type(tree_file):
    """

    :param tree_file:
    :return: type as determined by magic package
    """
    return magic.from_file(tree_file)

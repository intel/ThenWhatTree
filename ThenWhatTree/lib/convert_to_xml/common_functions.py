

# Copyright (C) 2018 Intel Corporation
# SPDX-License-Identifier: BSD-3-Clause

"""Module description here"""

# Import built in modules

# Import 3rd party modules
from xml.etree import ElementTree
from xml.dom import minidom

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

def create_root_element():
    return ElementTree.Element('node')


def _create_element_string(tree_element):
    return ElementTree.tostring(tree_element, encoding='utf-8', method='xml')


def get_xml_from_rootnode(rootnode):
    element_string = _create_element_string(rootnode)
    element_string_pretty = _make_pretty(element_string)
    return element_string_pretty


def create_subelement(parent_node, attributes):
    subelement = ElementTree.SubElement(parent_node, 'node')
    add_subelements_to_node(attributes, subelement)
    return subelement


def add_subelements_to_node(attributes, tree_element):
    for each_key in attributes:
        each_subelement = ElementTree.SubElement(tree_element, each_key)
        each_subelement.text = attributes[each_key]


def _make_pretty(element_string):
    """

    Args:
        element_string:

    Returns:

    """

    parsed_element = minidom.parseString(element_string)
    return parsed_element.toprettyxml(indent='    ')


def _convert_text_file_to_list(text_file):
    """

    :param text_file:
    :return:
    """
    # FIXME: This needs to be replaced with a call to a function that can handle
    # FIXME: zipped or unzipped files
    with open(text_file, 'r') as f:
        return [line.rstrip() for line in f]

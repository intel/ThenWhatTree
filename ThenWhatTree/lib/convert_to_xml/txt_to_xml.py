

# Copyright (C) 2018 Intel Corporation
# SPDX-License-Identifier: BSD-3-Clause

"""Module description here"""

# Import built in modules
import re

# Import 3rd party modules

# Import local modules
from ThenWhatTree.lib.convert_to_xml.common_functions import create_root_element, get_xml_from_rootnode, \
    create_subelement, add_subelements_to_node, _convert_text_file_to_list

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

def text_to_xml(text_file):
    """
    Generate a XML version of a decision tree from text file format.  The text file must represent parent-child
    relationships with a four space indentation.

    Args:
        text_file: path to a text file

    Returns:
        XML string of the decision tree

    """

    parents = {}
    text_list = _convert_text_file_to_list(text_file)
    depth, text = _parse_text_line(text_list[0])
    rootnode = create_root_element()
    add_subelements_to_node({'name': text}, rootnode)
    _update_parents(parents, rootnode)
    for line in text_list[1:]:
        _create_sub_element_from_line(line, parents)
    return get_xml_from_rootnode(rootnode)


def _create_sub_element_from_line(line, parents):
    """

    :param line:
    :param parents:
    :return:
    """
    depth, text = _parse_text_line(line)
    parent_node = get_parent_node(parents, depth)
    new_sub_element = create_subelement(parent_node, {'name': text})
    _update_parents(parents, new_sub_element, depth)


def get_parent_node(parents, depth):
    parent_depth = int(depth) - 1
    return parents[str(parent_depth)]


def _update_parents(parents, node, depth=0):
    """

    :param parents:
    :param depth:
    :param node:
    :return:
    """
    parents.update({str(depth): node})
    return parents


def _parse_text_line(line):
    """

    :param line:
    :return:
    """
    match = re.search("^(?P<space>\s*)(?P<text>\S+)", line)
    if len(match.group('space')) % int(4) != 0:
        raise Exception("Number of spaces at beginning of line not multiple of 4")
    return int(int(len(match.group('space'))) / int(4)), match.group('text')



# Copyright (C) 2018 Intel Corporation
# SPDX-License-Identifier: BSD-3-Clause

"""Module description here"""

# Import built in modules

# Import 3rd party modules

# Import local modules
from ThenWhatTree.lib.evaluate import get_node_element, has_node_element, _create_element_with_text
from ThenWhatTree.lib.exceptions import NoAttributeType, NoAttributeTypeName

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

def extract(tree_element):
    """
    Extract tree data and return a string

    :param tree_element: Root node instance of the tree_object
    :return: string containing annotated tree, node output, exceptions
    """
    output = ""
    tree_annotation = _get_tree_annotation(tree_element)
    if len(tree_annotation) > 0:
        output += tree_annotation
    tree_output = _get_tree_output(tree_element)
    if len(tree_output) > 0:
        output += '\n'
        output += 'Node output:\n'
        output += '------------\n'
        output += tree_output
    tree_exceptions = _get_tree_exceptions(tree_element)
    if len(tree_exceptions) > 0:
        output += '\n'
        output += 'Exceptions:\n'
        output += '-----------\n'
        output += tree_exceptions
    tree_exception_tb = _get_tree_exception_tb(tree_element)
    if len(tree_exception_tb) > 0:
        output += '\n'
        output += 'Exception traceback:\n'
        output += '--------------------\n'
        output += tree_exception_tb
    return output


def _get_tree_annotation(tree_element):
    """Generate a text version of a decision tree from XML file format.  Only the tree hierarchy is preserved.
    Any information stored in the NodeDetails class is lost in the text format.  Parent-child relationships
    are represented by a four space indentation

    Args:
        tree_element:

    Returns:
        Text version of the decision tree"""

    text_tree = ""
    my_tree = _add_depth_attribute_to_xml(tree_element)
    for elem in my_tree.iter('node'):
        result, index = get_result_for_node(elem)
        if result is not None:
            text_tree += ' ' * 4 * int(elem.find('depth').text) + index + elem.find('name').text + ' : ' + str(
                result) + '\n'
    return text_tree


def get_result_for_node(tree_element):
    if tree_element.find('name') is None:
        return ''
    index = ''
    if has_node_element(tree_element, 'exception'):
        result = get_node_element(tree_element, 'exception')
    elif has_node_element(tree_element, 'node_is_true'):
        result = get_node_element(tree_element, 'node_is_true')
        if result == 'true':
            index = '[' + str(get_node_element(tree_element, 'index')) + '] '
    else:
        result = None
    return result, index


def _get_tree_output(tree_element):
    if tree_element.find('name') is None:
        return ''
    if get_node_element(tree_element, 'node_is_true') == 'true':
        element_entry = '[' + str(get_node_element(tree_element, 'index')) + '] ' + get_node_element(tree_element, 'output') + '\n'
        return element_entry + ''.join([_get_tree_output(subnode) for subnode in tree_element])
    return ''


def _get_tree_exceptions(tree_element):
    if tree_element.find('name') is None:
        return ''
    element_entry = ''
    if has_node_element(tree_element, 'exception'):
        node_exception = get_node_element(tree_element, 'exception')
        element_entry = tree_element.find('name').text + ': ' + str(node_exception) + '\n'
    return element_entry + ''.join([_get_tree_exceptions(subnode) for subnode in tree_element])


def _get_tree_exception_tb(tree_element):
    if tree_element.find('name') is None:
        return ''
    element_entry = ''
    if has_node_element(tree_element, 'traceback'):
        node_exception = get_node_element(tree_element, 'traceback')
        element_entry = tree_element.find('name').text + ': ' + str(node_exception) + '\n'
    return element_entry + ''.join([_get_tree_exception_tb(subnode) for subnode in tree_element])


def _make_annotated_tree(tree_element, depth=0):
    if get_node_element(tree_element, 'node_is_true') == 'true':
        element_entry = ' ' * 4 * depth + '[' + str(
            get_node_element(tree_element, 'index')) + '] ' + tree_element.find('name').text + ': True\n'
        return element_entry + ''.join(
            [_make_annotated_tree(subnode, depth + 1) for subnode in tree_element.findall('node')])
    else:
        entry_indent = ' ' * (4 * depth + len('[ ] '))
        try:
            get_node_element(tree_element, 'exception')
        except (NoAttributeType, NoAttributeTypeName):
            return entry_indent + tree_element.find('name').text + ': False\n'
        return entry_indent + tree_element.find('name').text + ': Exception raised\n'


def _add_depth_attribute_to_xml(tree_element):
    """

    Args:
        tree_element:

    Returns:

    """
    depth = 0
    _add_depth_attribute_to_element(tree_element, depth)
    for child in tree_element:
        _add_depth_to_sub_elements(child, depth + 1)
    return tree_element


def _add_depth_to_sub_elements(element, depth):
    _add_depth_attribute_to_element(element, depth)
    for child in element.findall('node'):
        _add_depth_to_sub_elements(child, depth + 1)


def _add_depth_attribute_to_element(element, depth):
    depth_element = _create_element_with_text('depth', depth)
    element.append(depth_element)



# Copyright (C) 2018 Intel Corporation
# SPDX-License-Identifier: BSD-3-Clause

""" Contains functions for constructing and writing the ThenWhatTree node modules.  The create_node
function is invoked by the _create_tree function.  Functions are not expected to be used directly. """

# Import built in modules
import os

# Import 3rd party modules

# Import local modules
from ThenWhatTree.lib.exceptions import ElementNameError
from ThenWhatTree.lib.convert_to_xml.common_functions import create_subelement, add_subelements_to_node

# Module authorship metadata
from pathlib import Path

__author__ = "Erik W Berg"
__copyright__ = "Copyright 2018, Intel Corporation"
__credits__ = [""]
__license__ = "BSD-3-Clause"
__version__ = "1.0"
__maintainer__ = "Erik W Berg"
__email__ = ""
__status__ = "Production"  # Prototype, Development, Production

INDENT4 = '    '
INDENT8 = INDENT4 * 2


# Code starts here

def create_node(module_path, tree_element):
    """
    Called by the _create_tree method.  All elements of a decision tree node module are generated.  Method will
    look inside the lib_path/lib_name to find existing decision tree modules for each node.  If a node exists,
    the methods will inspect the module and extract any user generated code to include in the newly generated
    module.

    :param module_path: full path to the library where the subnode lives
    :param tree_element: Element object from the xml.etree.ElementTree package
    :return: None
    """

    tree_element = _standardize_tree_element(tree_element)
    if _node_does_not_exist(os.path.join(module_path, tree_element.find('name').text + '.py')):
        _create_node(module_path, tree_element)


def _standardize_tree_element(tree_element):
    """
    Make sure the element is well-formatted with a name subelement.  If the element does
    not have a 'name' subelement, create it based on the tag and change the tag to 'node'

    :param tree_element: ElementTree Element object
    :return: ElementTree Element object
    """
    if tree_element.tag == 'node':
        if tree_element.find('name') is not None:
            return tree_element
        elif tree_element.get('name') is not None:
            return _create_subelement_from_attribute(tree_element, tree_element.get('name'))
        else:
            pass
    else:
        if tree_element.find('name') or tree_element.get('name'):
            raise ElementNameError(tree_element.tag)
        else:
            return _create_name_subelement_from_tag(tree_element)


def _create_subelement_from_attribute(tree_element, attrib_name):
    attrib_value = tree_element.get(attrib_name)
    tree_element.attrib.pop(attrib_name)
    create_subelement(tree_element, attrib_name, attrib_value)
    return tree_element


def _create_name_subelement_from_tag(tree_element):
    name = tree_element.tag
    tree_element.tag = 'node'
    add_subelements_to_node({'name': name}, tree_element)
    return tree_element


def _create_node(module_path, tree_element):
    """Constructs a list of strings comprising the sections of the node module.  Node module file is written.

    :param module_path: full path to the library where the subnode lives
    :param tree_element: Element object from the xml.etree.ElementTree package
    :return: None
    """
    module_text = _create_header()
    module_text += _create_imports() + ['\n']
    module_text += _create_class(tree_element) + ['\n']
    module_text += _create_is_true() + ['\n']
    module_text += _create_unittest(tree_element) + ['\n']
    _write_node_file(module_path, tree_element.find('name').text + '.py', module_text)


def _write_node_file(module_path, file_name, module_text):
    """
    Write the module for the decision tree node.

    :param module_path: full path to the library where the subnode lives
    :param file_name: tag attribute of Element object from the xml.etree.ElementTree package
    :param module_text: list of strings comprising the module for a decision tree node
    :return: None
    """

    if not os.path.exists(module_path):
        os.makedirs(module_path)
    with open(os.path.join(module_path, file_name), 'w') as node_file:
        node_file.write('\n'.join(module_text))


def _create_header():
    """

    :return: list comprised of any header information
    """
    header_string = "# Copyright (C) 2018 Intel Corporation\n"
    header_string += "# SPDX-License-Identifier: BSD-3-Clause\n"
    return [header_string]


def _create_class(tree_element):
    """
    Create the class definition for the module.  Class name is the tag attribute of the tree_element

    :param tree_element: Element object from the xml.etree.ElementTree package
    :return: single element list with the node class name
    """

    return ['class ' + tree_element.find('name').text + '(ThenWhatTreeNode):']


def _create_is_true():
    """
    Create the is_true for the initial node definition.  Default behavior is to raise a NotImplementedError exception

    :return: list containing strings for default is_true source code
    """
    return [INDENT4 + 'def is_true(self):',
            INDENT8 + 'raise NotImplementedError']


# noinspection PyListCreation
def _create_unittest(tree_element):
    """
    Create unittest infrastructure for module

    :param tree_element: Element object from the xml.etree.ElementTree package
    :return: list containing default unit test code for module
    """

    unittest_class = ['\n\n']
    unittest_class.append('class MyTestCase(unittest.TestCase):')
    unittest_class.append('')
    unittest_class.append(INDENT4 + 'def setUp(self):')
    unittest_class.append(INDENT8 + 'pass')
    unittest_class.append('')
    unittest_class.append(INDENT4 + '# REQUIRED FOR VASE - DO NOT EDIT THIS METHOD')
    unittest_class.append(INDENT4 + 'def test_instantiateScript(self):')
    unittest_class.append(INDENT8 + 'myClass = ' + tree_element.find('name').text + '()')
    unittest_class.append('')
    unittest_class.append(INDENT4 + '# ADD USER UNITTESTS HERE')
    unittest_class.append('')
    unittest_class.append('')
    unittest_class.append('if __name__ == \'__main__\':')
    unittest_class.append(INDENT4 + 'unittest.main()')
    return unittest_class


def _node_does_not_exist(node_path):
    """
    Determine whether module already exists for node

    :param node_path: full path to node module
    :return: bool; True if node does not exist; False if it does exist
    """

    try:
        # noinspection PyArgumentList
        Path(node_path).resolve()
    except FileNotFoundError:
        return True
    else:
        return False


# noinspection PyListCreation
def _create_imports():
    """
    Create the import required by the module

    :return: list containing strings for module imports
    """
    detect_imports = ['import unittest']
    detect_imports.append('from ThenWhatTree import ThenWhatTreeNode')
    return detect_imports

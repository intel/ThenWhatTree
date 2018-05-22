# Copyright (C) 2018 Intel Corporation
# SPDX-License-Identifier: BSD-3-Clause

"""Module description here"""

# Import built in modules
import inspect
import sys
import threading

# noinspection PyPep8Naming
from xml.etree import ElementTree as ET

# Import local modules
from ThenWhatTree.lib.create_tree import get_tree_root_element, create_tree_object_from_xml
from ThenWhatTree.lib.exceptions import NoClassesFoundInModule, ThenWhatTreeNodeSubclassNotFound, NoAttributeType, \
    NoAttributeTypeName, BranchElementError, CouldNotDiscoverCpus

# Import 3rd party modules

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

NUM_TRUE = -1
NUM_CPUS = 1


def evaluate(xml_file):
    """
    Function for evaluating an xml file.  Assumption is that the ThenWhatTreeNode modules
    have been created already.  Function will walk the tree and go deeper when a node
    evaluates to 'true' and abort a branch of the tree if a node evaluates to 'false.

    Simple mantra to remember: "If true, go deeper"

    :param xml_file: xml file consisting of elements with 'node' tag
    :return: ElementTree object
    """
    lib_path = xml_file.rsplit('/', 1)[0]
    _add_node_library_to_path(lib_path)
    _set_NUM_CPUS()
    tree_object = create_tree_object_from_xml(xml_file)
    tree_root_element = get_tree_root_element(tree_object)
    _move_attributes_to_node_elements(tree_root_element)
    _evaluate_tree_element(tree_root_element)
    _evaluate_tree(tree_root_element)
    return tree_object


def _set_NUM_CPUS():
    try:
        import multiprocessing
        global NUM_CPUS
        NUM_CPUS = multiprocessing.cpu_count()
    except (ImportError, NotImplementedError):
        pass


def _add_node_library_to_path(lib_path):
    """
    Function to add the path of the ThenWhatTree node library to sys.path
    :param lib_path: directory path
    :return: None
    """
    sys.path.append(lib_path)


class EvaluateTreeThread(threading.Thread):
    def __init__(self, subnode):
        threading.Thread.__init__(self)
        self.name = subnode.find('name').text
        self.subnode = subnode

    def run(self):
        _evaluate_tree_element(self.subnode)

    def get_name(self):
        return self.name


def _evaluate_tree(tree_element):
    """
    Function used for walking the tree.
    1) Evaluate the node element
    2) If the 'node_is_true' subelement is 'true':
        i)  add an element with the global hint index
        ii) for each of the subnodes of the element:
            a) set the branch elements of the node element in the subnodes
            b) recursively call the function on each subnode
    3) If the 'node_is_true' subelement is 'false', take no action

    :param tree_element: Element object from the ElementTree package
    :return: None
    """
    # _evaluate_tree_element(tree_element)
    if get_node_element(tree_element, 'node_is_true') == 'true':
        _add_hint_index_to_tree_element(tree_element)
        subnode_thread_list = []
        for subnode in _get_element_subnodes(tree_element):
            set_branch_elements_in_children(tree_element, subnode)
            subnode_thread_list.append(EvaluateTreeThread(subnode))
        for index in range(0, len(subnode_thread_list) + 1, NUM_CPUS):
            for subnode_thread in subnode_thread_list[index:index + NUM_CPUS]:
                subnode_thread.start()
            for subnode_thread in subnode_thread_list[index:index + NUM_CPUS]:
                subnode_thread.join()
        for subnode in _get_element_subnodes(tree_element):
            _evaluate_tree(subnode)


def _get_element_subnodes(tree_element):
    """
    Get all of the sublements of the tree_element with a 'node' tag

    :param tree_element: Element object from the ElementTree package
    :return: From ElementTree documentation:  "Returns a list of all matching
    elements in document order."
    """
    return tree_element.findall('node')


def _add_hint_index_to_tree_element(tree_element):
    """
    A global counter is used to keep track of the hint indexes.

    :param tree_element: Element object from the ElementTree package
    :return: None
    """
    global NUM_TRUE
    NUM_TRUE += 1
    set_node_element(tree_element, 'index', NUM_TRUE)


def _evaluate_tree_element(tree_element):
    """
    Find the correct instance of the node for this tree_element.  Raise exception if none
    was found.  Evaluate the instance of the node.

    :param tree_element: Element object from the ElementTree package
    :return: None
    """
    try:
        node_instance = _get_node_instance(tree_element)
    except ModuleNotFoundError as inst:
        set_node_element(tree_element, 'exception', inst)
        set_node_element(tree_element, 'node_is_true', 'false')
    else:
        node_instance.evaluate_node()


def _move_attributes_to_node_elements(tree_element):
    """
    All attributes are converted to elements.  This is to facilitate easier output formatting
    of the fully evaluated xml file.

    :param tree_element: Element object from the ElementTree package
    :return: None
    """
    _create_node_elements_from_xml_attrib(tree_element)
    for subnode in tree_element:
        _move_attributes_to_node_elements(subnode)


def _create_node_elements_from_xml_attrib(tree_element):
    """
    FIXME:  Looks like there might be a bug here...why is there a return if
    the tree_element doesn't have any attributes?  Seems like it not return since
    this function is called by a recursive function that expects to walk the entire tree.

    Every attribute of the tree_element is converted to subelement.

    :param tree_element: Element object from the ElementTree package
    :return: None
    """
    if not tree_element.attrib:
        return
    xml_attributes = tree_element.attrib
    if 'name' not in xml_attributes.keys():
        # FIXME - needs a better exception
        raise Exception
    tree_element.attrib = {}
    for xml_attrib in xml_attributes.keys():
        new_element = _create_element_with_text(xml_attrib, xml_attributes[xml_attrib])
        tree_element.append(new_element)


def _create_element_with_text(element_tag, element_text):
    """
    Function to create a new ElementTree Element with a text field

    :param element_tag: tag field in the Element
    :param element_text: text for the specified tag field
    :return: ElementTree Element
    """
    new_element = ET.Element(element_tag)
    new_element.text = element_text
    return new_element


def _create_element_with_attribute(element_tag, key, value):
    """
    Function to create a new ElementTree Element with an attribute

    :param element_tag: tag field in the Element
    :param key: attribute key
    :param value: attribute value
    :return: ElementTree Element
    """
    new_element = ET.Element(element_tag)
    new_element.set(key, value)
    return new_element


def set_node_element(tree_element, tag, text, value=None):
    """
    FIXME:  This is an ugly function that should be refactored.  It wqs written to create the same
    function for setting either an attribute or a subelement for an element.

    :param tree_element: Element object from the ElementTree package
    :param tag: attribute name to be set in the 'branch' element or element name to be set in tree_element
    :param text: value for subelement
    :param value: value for attribute
    :return: None
    """
    if value is not None:
        branch_elements = tree_element.findall(tag)
        for each_element in branch_elements:
            if text in each_element.attrib.keys():
                each_element.attrib[text] = value
                return
        new_element = _create_element_with_attribute(tag, text, value)
        tree_element.append(new_element)

    existing_element = tree_element.find(tag)
    if existing_element is not None:
        existing_element.text = text
    else:
        new_element = _create_element_with_text(tag, text)
        tree_element.append(new_element)


def has_node_element(tree_element, tag):
    """
    Function to test if a tree_element has a subelement with the specified tag

    :param tree_element: Element object from the ElementTree package
    :param tag: subelement being searched for
    :return: bool
    """
    try:
        get_node_element(tree_element, tag)
    except (NoAttributeType, NoAttributeTypeName):
        return False
    return True


def get_node_element(tree_element, tag, key=None):
    """
    FIXME:  This is an ugly function that should be refactored.  It wqs written to create the same
    function for getting either an attribute or a subelement for an element.

    :param tree_element: Element object from the ElementTree package
    :param tag: subelement of the tree_element
    :param key: key for value to be returned from the 'branch' subelements
    :return: either text from the element or value from the attribute
    """
    if key:
        branch_elements = tree_element.findall('branch')
        for each_element in branch_elements:
            if key in each_element.attrib.keys():
                return each_element.attrib[key]
        raise BranchElementError(tree_element.find('name').text, key)
    if tree_element.find(tag) is not None:
        text = tree_element.find(tag).text
        return text
    else:
        raise NoAttributeTypeName(tree_element.find('name').text, tag)


def set_branch_elements_in_children(tree_element, subnode):
    """
    Function to identify and pass all the 'branch' elements of the tree_element to
    its children.

    :param tree_element: Element object from the ElementTree package
    :param subnode: Element object from the ElementTree package
    :return: None
    """
    branch_elements = tree_element.findall('branch')
    for each_element in branch_elements:
        key = each_element.keys()[0]
        value = each_element.get(key)
        set_node_element(subnode, 'branch', key, value)


# noinspection PyPep8Naming
def _get_node_instance(tree_element):
    """
    For a given tree_element:
    1) import the module for this element
    2) find all of the classes in the module
    3) filter to find the class that is a subnode of ThenWhatTreeNode class
    4) return the instance of the class

    :param tree_element: Element object from the ElementTree package
    :return: instance of ThenWhatTreeNode for tree_element
    """
    _import_module_for_tree_element(tree_element)
    classes_in_module = _get_node_classes(tree_element)
    ThenWhatTreeNode_subclass = _get_ThenWhatTreeNode_subclass(classes_in_module)
    return ThenWhatTreeNode_subclass(tree_element)


# noinspection PyPep8Naming
def _get_ThenWhatTreeNode_subclass(classes_in_module):
    """
    Inspects a list of classes and returns the first class type object that is a subclass of
    ThenWhatTreeNode.  Only one subclass of ThenWhatTreeNode is expected.

    The inspect.getmro will return a tuple of the class inheritance structure for 'each_class'.
    It is assumed that the [1] entry in that tuple is the parent class.  By looking for the class
    that has ThenWhatTreeNode as a parent, we can identify the correct class to instantiate.

    :param classes_in_module:  list of class type objects
    :return: class type object
    """
    for each_class in classes_in_module:
        class_inheritance_tuple = inspect.getmro(each_class[1])
        if class_inheritance_tuple[1].__name__ == 'ThenWhatTreeNode':
            return each_class[1]
    raise ThenWhatTreeNodeSubclassNotFound(classes_in_module)


def _get_node_classes(tree_element):
    """
    Use inspect to find all the classes in the module with the same name as the tree_element

    :param tree_element: Element object from the ElementTree package
    :return: list of class type objects
    """
    classes_in_module = inspect.getmembers(sys.modules[tree_element.find('name').text], inspect.isclass)
    if not classes_in_module:
        raise NoClassesFoundInModule(tree_element.find('name').text)
    return classes_in_module


def _import_module_for_tree_element(tree_element):
    """
    Imports the module in the current directory with the same name as the tree_element

    :param tree_element: Element object from the ElementTree package
    :return: None
    """
    # FIXME get unit test around this for the case when we try to import something that doesn't exist
    exec("import {}".format(tree_element.find('name').text))

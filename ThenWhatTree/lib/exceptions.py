

# Copyright (C) 2018 Intel Corporation
# SPDX-License-Identifier: BSD-3-Clause

"""Module description here"""

# Import built in modules

# Import 3rd party modules

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

class ThenWhatTreeException(Exception):
    pass


class CouldNotDiscoverCpus(ThenWhatTreeException):
    def __init__(self):
        self.message = "Could not discover number of CPUs"


class ParentNotFoundError(ThenWhatTreeException):
    """ Branch attribute was accessed without assignment. """

    def __init__(self, parent):
        self.message = "Node: \'" + parent + \
                       "\' not defined in sped file prior to reference"


class NoParentGiven(ThenWhatTreeException):
    pass


class BranchElementError(ThenWhatTreeException):
    """ Branch attribute was accessed without assignment. """

    def __init__(self, node_name, element):
        self.message = "Branch element: \'" + element + \
                       "\' not assigned with \'set_branch_element\' by any ancestor of " + node_name


class ElementNameError(ThenWhatTreeException):
    """ Branch attribute was accessed without assignment. """

    def __init__(self, element):
        self.message = "Element: \'" + element + \
                       "\' is not named \'node\' and has a \'name\' field"


class XmlAttributeError(ThenWhatTreeException):
    """ XML attribute was accessed without assignment. """

    def __init__(self, node_name, attribute):
        self.message = "XML attribute: \'" + attribute + "\' not assigned for " + node_name


class MetaDataAttributeError(ThenWhatTreeException):
    """ Metadata attribute was accessed without assignment. """

    def __init__(self, node_name, attribute):
        self.message = "Metadata attribute: \'" + attribute + "\' not assigned for " + node_name


class UnsupportedFileType(ThenWhatTreeException):
    """ Input file type is unsupported. """

    def __init__(self, file, file_type):
        self.message = "File type must be XML or ASCII text.\n" + file + ' is of type: ' + file_type


class NoClassesFoundInModule(ThenWhatTreeException):
    """ Module does not contain any classes. """

    def __init__(self, module_name):
        self.message = "No classes found in module: " + module_name


class ThenWhatTreeNodeSubclassNotFound(ThenWhatTreeException):
    """ Module does not contain any subclasses of ThenWhatTreeNode. """

    def __init__(self, classes_in_module):
        self.message = "Could not find a subclass of 'ThenWhatTreeNode' in " + ",".join(
            [x[0] for x in classes_in_module])


class NoAttributeType(ThenWhatTreeException):
    """ Attribute type could not be found for the XML node. """

    def __init__(self, node, attrib_type):
        self.message = node + " does not have attribute: " + attrib_type


class NoAttributeTypeName(ThenWhatTreeException):
    """ Attribute name could not be found in the attribute type for the XML node. """

    def __init__(self, node, attrib_name):
        self.message = node + " does not have attribute: " + attrib_name


class MissingDataEntries(ThenWhatTreeException):
    """ Length of fields in a CSV line is less than the number of column headers """

    def __init__(self, fields, data):
        self.message = "Length mismatch discovered between:" + fields + "\n" + data

class NonAlphaNumericCharacters(ThenWhatTreeException):
    """ Field should not cantain non-alphanumeric characters """

    def __init__(self, field, my_string):
        self.message = "Field '" + field + "' should only contain alphanumeric characters or ' ' or '_':" + my_string + "\n"

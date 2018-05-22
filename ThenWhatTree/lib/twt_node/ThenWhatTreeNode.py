

# Copyright (C) 2018 Intel Corporation
# SPDX-License-Identifier: BSD-3-Clause

"""Base class for all ThenWhatTree nodes"""

# Import built in modules
import sys
import traceback

# Import local modules
from ThenWhatTree.lib.evaluate import get_node_element
from ThenWhatTree.lib.evaluate import set_node_element
from ThenWhatTree.lib.exceptions import BranchElementError, XmlAttributeError

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

class ThenWhatTreeNode(object):

    def __init__(self, tree_element, **kwargs):
        self.tree_element = tree_element
        self.kwargs = kwargs
        self._output = ''

    ###################################################################################
    # Externally visible

    # noinspection PyMethodMayBeStatic
    def is_true(self):
        raise NotImplementedError

    def set_branch_element(self, key, value):
        set_node_element(self.tree_element, 'branch', key, value)

    def get_branch_element(self, key):
        return get_node_element(self.tree_element, 'branch', key)

    @property
    def output(self):
        if not self._output:
            return self.__class__.__name__ + " is " + str(self.get_element('node_is_true'))
        else:
            return self._output

    @output.setter
    def output(self, message):
        self._output = message

    ###################################################################################
    # Internal use

    def get_element(self, key):
        return get_node_element(self.tree_element, key)

    def set_element(self, key, value):
        set_node_element(self.tree_element, key, value)

    def evaluate_node(self):
        self.evaluate_node_is_true()
        if self.get_element('node_is_true') == 'true':
            self.set_element('output', self.output)
            self.evaluate_user_defined_methods()

    def evaluate_node_is_true(self):
        try:
            node_is_true = str(self.is_true()).lower()
        except NotImplementedError:
            node_is_true = 'false'
            self.set_element('exception', 'NotImplementedError')
        except (BranchElementError, XmlAttributeError) as inst:
            node_is_true = 'false'
            self.set_element('exception', repr(inst.message))
        except Exception as inst:
            node_is_true = 'false'
            a, b, tb = sys.exc_info()
            self.set_element('exception', repr(inst))
            self.set_element('traceback', traceback.format_tb(tb))
        self.set_element('node_is_true', node_is_true)

    def evaluate_user_defined_methods(self):
        pass


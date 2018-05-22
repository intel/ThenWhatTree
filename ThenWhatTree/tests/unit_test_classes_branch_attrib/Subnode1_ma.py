

# Copyright (C) 2018 Intel Corporation
# SPDX-License-Identifier: BSD-3-Clause

import unittest
from ThenWhatTree import ThenWhatTreeNode


class Subnode1_ma(ThenWhatTreeNode):


    def is_true(self):
        self.set_branch_element('dummy_key', 'dummy_value')
        # print(self.__class__.__name__ + ": Output override")
        self.output = self.__class__.__name__ + ": Output override"
        # FIXME:  would be great to be able to unittest this scenario where
        # FIXME:  the property was invoked as a function instead as an assignment
        # self.output(self.__class__.__name__ + ": Output override")
        return True





class MyTestCase(unittest.TestCase):

    def setUp(self):
        pass

    # REQUIRED FOR VASE - DO NOT EDIT THIS METHOD
    def test_instantiateScript(self):
        myClass = Subnode1_ma()

    # ADD USER UNITTESTS HERE


if __name__ == '__main__':
    unittest.main()




# Copyright (C) 2018 Intel Corporation
# SPDX-License-Identifier: BSD-3-Clause

import unittest
from ThenWhatTree import ThenWhatTreeNode


class Subnode4_ma(ThenWhatTreeNode):



    def is_true(self):
        self.get_xml_attribute('test_xml_attr')
        return True





class MyTestCase(unittest.TestCase):

    def setUp(self):
        pass

    # REQUIRED FOR VASE - DO NOT EDIT THIS METHOD
    def test_instantiateScript(self):
        myClass = Subnode4_ma()

    # ADD USER UNITTESTS HERE


if __name__ == '__main__':
    unittest.main()


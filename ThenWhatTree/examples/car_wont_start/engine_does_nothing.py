# Copyright (C) 2018 Intel Corporation
# SPDX-License-Identifier: BSD-3-Clause

import unittest
from ThenWhatTree import ThenWhatTreeNode


class engine_does_nothing(ThenWhatTreeNode):


    def is_true(self):
        raise NotImplementedError





class MyTestCase(unittest.TestCase):

    def setUp(self):
        pass

    # REQUIRED FOR VASE - DO NOT EDIT THIS METHOD
    def test_instantiateScript(self):
        myClass = engine_does_nothing()

    # ADD USER UNITTESTS HERE


if __name__ == '__main__':
    unittest.main()


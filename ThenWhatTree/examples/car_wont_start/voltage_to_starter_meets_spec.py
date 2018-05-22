# Copyright (C) 2018 Intel Corporation
# SPDX-License-Identifier: BSD-3-Clause

import unittest
from ThenWhatTree import ThenWhatTreeNode


class voltage_to_starter_meets_spec(ThenWhatTreeNode):


    def is_true(self):
        return True


class MyTestCase(unittest.TestCase):

    def setUp(self):
        pass

    # REQUIRED FOR VASE - DO NOT EDIT THIS METHOD
    def test_instantiateScript(self):
        myClass = voltage_to_starter_meets_spec()

    # ADD USER UNITTESTS HERE


if __name__ == '__main__':
    unittest.main()


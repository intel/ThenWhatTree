# Copyright (C) 2018 Intel Corporation
# SPDX-License-Identifier: BSD-3-Clause

import unittest
from ThenWhatTree import ThenWhatTreeNode


class battery_needs_charging(ThenWhatTreeNode):


    def is_true(self):
        return 1/0


class MyTestCase(unittest.TestCase):

    def setUp(self):
        pass

    # REQUIRED FOR VASE - DO NOT EDIT THIS METHOD
    def test_instantiateScript(self):
        myClass = battery_needs_charging()

    # ADD USER UNITTESTS HERE


if __name__ == '__main__':
    unittest.main()


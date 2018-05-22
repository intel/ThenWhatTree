

# Copyright (C) 2018 Intel Corporation
# SPDX-License-Identifier: BSD-3-Clause

import time
import unittest
from ThenWhatTree import ThenWhatTreeNode


class Subnode13(ThenWhatTreeNode):


    def is_true(self):
        time.sleep(.1)
        return 1/0
        # raise NotImplementedError





class MyTestCase(unittest.TestCase):

    def setUp(self):
        pass

    # REQUIRED FOR VASE - DO NOT EDIT THIS METHOD
    def test_instantiateScript(self):
        myClass = Subnode13()

    # ADD USER UNITTESTS HERE


if __name__ == '__main__':
    unittest.main()


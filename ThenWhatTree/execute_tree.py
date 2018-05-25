#!/usr/bin/env python3


# Copyright (C) 2018 Intel Corporation
# SPDX-License-Identifier: BSD-3-Clause

"""Function for evaluating the nodes of a decision tree and extracting out the results from each of the nodes."""

# Import built in modules
import argparse
import sys
import os

# Import 3rd party modules

# Import local modules
from ThenWhatTree import _get_file_type
from ThenWhatTree import evaluate
from ThenWhatTree import extract

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


def parse_args():
    '''
    Function to parse the cmdline, check that required args are present and that the file types are correct

    :return:
    '''
    parser = argparse.ArgumentParser()
    parser.add_argument('--xml', help='path to xml file defining the decision tree', nargs='?', type=str)
    args = parser.parse_args()
    check_cmd_line_args(args)
    check_xml_file_type(args)
    return args

def check_cmd_line_args(args):
    '''
    Raise an exception if an XML file was not passed in on the cmd line.
    :param args:
    :return: none
    '''
    if not args.xml:
        raise Exception('--xml switch must be populated')


def check_xml_file_type(args):
    '''
    Raise an exception if the cmd line switch does not match the type of the passed file

    :param args:
    :return: none
    '''
    if 'XML' not in _get_file_type(args.xml):
        raise Exception(sys.argv[1] + ' is not a XML file')


if __name__ == '__main__':

    args = parse_args()
    os.environ['PYTHONDONTWRITEBYTECODE'] = 'TRUE'
    tree_object = evaluate(args.xml)
    print(extract(tree_object.getroot()))

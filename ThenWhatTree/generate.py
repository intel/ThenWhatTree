#!/usr/bin/env python3

# Copyright (C) 2018 Intel Corporation
# SPDX-License-Identifier: BSD-3-Clause

"""Module is used to generate XML version of a decision tree
and the library of python modules that represent the tree"""

# Import built in modules
import argparse
import sys
import os

# Import 3rd party modules

# Import local modules
from ThenWhatTree import _get_file_type, csv_to_xml, text_to_xml, xml_to_tree, _write_file_to_directory

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

    :return: args
    '''

    parser = argparse.ArgumentParser()
    parser.add_argument('--csv', help='path to csv file defining a decision tree', nargs='?', type=str)
    parser.add_argument('--lib', help='path to library where collateral will be created', nargs='?', type=str)
    parser.add_argument('--text', help='path to text file defining a decision tree', nargs='?', type=str)
    parser.add_argument('--xml', help='path to xml file defining a decision tree', nargs='?', type=str)
    args = parser.parse_args()
    check_cmd_line_args(args)
    check_file_type(args)
    return args

def check_cmd_line_args(args):
    '''
    Raise an exception if a csv, text or xml file is not passed on the cmd line

    :param args:
    :return: none
    '''
    if not (args.csv or args.text or args.xml):
        raise Exception('--csv or --text or --xml switch must be populated')


def check_file_type(args):
    '''
    Raise an exception if the cmd line switch does not match the type of the passed file
    :param args:
    :return: none
    '''
    if args.csv and 'text' not in _get_file_type(args.csv):
        raise Exception(sys.argv[1] + ' is not a text file')
    if args.text and 'text' not in _get_file_type(args.text):
        raise Exception(sys.argv[1] + ' is not a text file')
    if args.xml and 'XML' not in _get_file_type(args.xml):
        raise Exception(sys.argv[1] + ' is not a XML file')

def generate(args):
    '''
    Two steps:
    1) invoke method to generate the xml
    2) build the node library from the generated xml

    :param args:
    :return: none
    '''
    src_file, xml_file = generate_xml(args)
    if args.lib:
        xml_to_tree(xml_file, args.lib)
        _write_file_to_directory(src_file, args.lib)

def generate_xml(args):
    '''
    Function will generate an XML file from the src file passed on the command line.  Depending on which
    type of file is passed on the cmd line, different XML generator functions will be called.
    :param args:
    :return:
        src_file: file used to generate the xml
        xml_file: generated file
    '''
    my_xml = ''
    xml_file = ''
    src_file = None
    if args.xml:
        return args.xml, args.xml
    if args.csv:
        src_file = args.csv
        xml_file = os.path.splitext(args.csv)[0] + '.xml'
        my_xml = csv_to_xml(args.csv)
    elif args.text:
        src_file = args.text
        xml_file = os.path.splitext(args.text)[0] + '.xml'
        my_xml = text_to_xml(args.text)

    with open(xml_file, 'w') as f:
        f.write(my_xml)
    return src_file, xml_file


if __name__ == '__main__':

    os.environ['PYTHONDONTSETBYTECODE'] = 'TRUE'
    args = parse_args()
    generate(args)

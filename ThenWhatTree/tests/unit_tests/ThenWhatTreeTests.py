

# Copyright (C) 2018 Intel Corporation
# SPDX-License-Identifier: BSD-3-Clause

"""Module description here"""

import filecmp
import os
import shutil
# Import built in modules
import unittest

# Import local modules
from ThenWhatTree.lib import create_tree
from ThenWhatTree import text_to_xml, csv_to_xml
from ThenWhatTree.lib import evaluate, extract
from ThenWhatTree.lib.exceptions import BranchElementError, ElementNameError, ParentNotFoundError, MissingDataEntries, \
    NonAlphaNumericCharacters
from ThenWhatTree.lib.twt_node.create_node import _standardize_tree_element

from xml.etree import ElementTree as ET
from ThenWhatTree.lib.convert_to_xml.common_functions import _make_pretty, _create_element_string, get_xml_from_rootnode
import ThenWhatTree.lib.convert_to_xml.csv_to_xml as csv_to_xml_module
# from ThenWhatTree.lib.convert_to_xml.csv_to_xml import _get_fields_with_values, remove_spaces_from_values, \
#     check_keys_for_bad_characters, FIELDS_WITHOUT_SPACES

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

class MyTestCase(unittest.TestCase):
    def setUp(self):
        self.setToTrue = lambda: 'true'
        self.raiseException = lambda: (_ for _ in ()).throw(Exception("Exception found"))
        import sys, re
        sys.path = [x for x in sys.path if not re.search('\.local', x)]
        sys.path = [x for x in sys.path if not re.search('egg', x)]
        import ThenWhatTree.lib.ElementTree_extension

    def test_add_branch_attribute_for_subnodes(self):
        xml_file = '../unit_test_classes_tags/Rootnode_add_branch_attr.xml'
        tree = evaluate.evaluate(xml_file)
        for subnode in tree.iter('node'):
            if subnode.find('name').text in ['Subnode31', 'Subnode32']:
                with self.assertRaises(BranchElementError):
                    evaluate.get_node_element(subnode, 'branch', 'test')
            else:
                name = subnode.find('name').text
                node_element = evaluate.get_node_element(subnode, 'branch', 'test')
                self.assertEqual(node_element, 'value')

    def test_get_tree_annotation(self):
        import time
        start = time.time()
        evaluate.NUM_TRUE = -1
        xml_file = '../unit_test_classes_tags/Rootnode.xml'
        tree_object = evaluate.evaluate(xml_file)
        tree_annotation = extract._get_tree_annotation(tree_object.getroot())
        # tree_annotation = extract.extract(tree_object.getroot())
        # print(tree_annotation)
        expected_annotation = ""
        expected_annotation += "[0] Rootnode : true\n"
        expected_annotation += "    [1] Subnode1 : true\n"
        expected_annotation += "        [2] Subnode11 : true\n"
        expected_annotation += "        Subnode12 : NotImplementedError\n"
        expected_annotation += "        Subnode13 : ZeroDivisionError('division by zero',)\n"
        expected_annotation += "    Subnode2 : false\n"
        expected_annotation += "    Subnode3 : NotImplementedError\n"
        self.assertEqual(tree_annotation, expected_annotation)
        end = time.time()
        self.assertLess(end - start, 0.4)

    def test_get_tree_full_output(self):
        xml_file = '../unit_test_classes_tags/Rootnode.xml'
        tree_object = evaluate.evaluate(xml_file)
        tree_annotation = extract.extract(tree_object.getroot())


    # def test_kwargs(self):
    #     my_dict = {'key1': 5, 'key2': '0x1'}
    #     self.kwargs = ThenWhatTree.tests.unit_test_classes_2.Rootnode.Rootnode(my_kwarg=my_dict)
    #     evaluate.instantiate_tree_from_rootnode(self.kwargs)
    #     evaluate._evaluate_tree(self.kwargs)
    #     self.assertEqual(self.kwargs.subnodes[2].subnodes[1].my_kwarg['key1'], 5)
    #     self.assertEqual(self.kwargs.subnodes[2].subnodes[1].my_kwarg['key2'], '0x1')

    def test_get_file_type(self):
        self.assertEqual(create_tree._get_file_type('../unit_test_classes_branch_attrib/Rootnode_ma.xml'), 'XML')
        self.assertEqual(create_tree._get_file_type('../unit_test_classes_branch_attrib/Rootnode_ma.txt'), 'ASCII text')
        # with self.assertRaises(UnsupportedFileType):
        #     self.assertEqual(create_tree._get_file_type('../unit_test_classes_branch_attrib/Rootnode_ma.py'), 'ASCII text')


    def test_create_node_elements_from_xml_attrib(self):
        tree_object = evaluate.create_tree_object_from_xml('../unit_test_classes_branch_attrib/Rootnode_ma.xml')
        tree_root_element = evaluate.get_tree_root_element(tree_object)
        self.assertEqual(tree_root_element.attrib, {'name': 'Rootnode_ma', 'register': 'Rootnode_ma_REG'})
        evaluate._create_node_elements_from_xml_attrib(tree_root_element)
        self.assertEqual(tree_root_element.attrib, {})
        self.assertEqual(evaluate.get_node_element(tree_root_element, 'register'), 'Rootnode_ma_REG')
        self.assertEqual(evaluate.get_node_element(tree_root_element, 'name'), 'Rootnode_ma')

    def test_move_xml_attr_to_node_elements(self):
        tree_object = evaluate.create_tree_object_from_xml('../unit_test_classes_branch_attrib/Rootnode_ma.xml')
        tree_root_element = evaluate.get_tree_root_element(tree_object)
        self.assertEqual(tree_root_element.attrib, {'name': 'Rootnode_ma', 'register': 'Rootnode_ma_REG'})
        evaluate._move_attributes_to_node_elements(tree_root_element)
        register_element = tree_root_element.find('register')
        self.assertEqual(register_element.text, 'Rootnode_ma_REG')
        self.assertEqual(tree_root_element.attrib, {})

    def test_set_element(self):
        tree_object = evaluate.create_tree_object_from_xml('../unit_test_classes_branch_attrib/Rootnode_ma.xml')
        tree_root_element = evaluate.get_tree_root_element(tree_object)
        evaluate._move_attributes_to_node_elements(tree_root_element)
        my_element = tree_root_element.find('register')
        self.assertEqual(my_element.text, 'Rootnode_ma_REG')
        # evaluate.set_node_element(tree_root_element, 'something', 'something_text')
        # my_element = tree_root_element.find('something')
        # self.assertEqual(my_element.text, 'something_text')
        evaluate.set_node_element(tree_root_element, 'register', 'different')
        my_element = tree_root_element.find('register')
        self.assertEqual(my_element.text, 'different')


    def test_get_tree_exceptions(self):
        xml_file = '../unit_test_classes_tags/Rootnode.xml'
        tree_object = evaluate.evaluate(xml_file)
        tree_output = extract._get_tree_exceptions(tree_object.getroot())
        expected_exceptions = "Subnode12: NotImplementedError\nSubnode13: ZeroDivisionError('division by zero',)\nSubnode3: NotImplementedError\n"
        self.assertEqual(tree_output, expected_exceptions)

    def test_get_tree_output(self):
        evaluate.NUM_TRUE = -1
        xml_file = '../unit_test_classes_tags/Rootnode.xml'
        my_tree_object = evaluate.evaluate(xml_file)
        my_tree_output = extract._get_tree_output(my_tree_object.getroot())
        expected_output = "[0] Rootnode is true\n[1] Subnode1 is true\n[2] Subnode11 is true\n"
        self.assertEqual(my_tree_output, expected_output)

    def test_xml_to_tree(self):
        xml_file = '../unit_test_classes_gen/Rootnode.xml'
        test_dir = '../unit_test_classes_gen'
        gen_dir = '/tmp/ThenWhatTree'
        if os.path.exists(gen_dir):
            shutil.rmtree(gen_dir)
        create_tree.xml_to_tree(xml_file, gen_dir)
        directory_compare = filecmp.dircmp(test_dir, gen_dir)
        self.assertEqual(directory_compare.diff_files, [])
        self.assertEqual(directory_compare.right_only, [])
        self.assertEqual(directory_compare.left_only, [])
        if os.path.exists(os.path.join(gen_dir, 'Rootnode.py')):
            os.remove(os.path.join(gen_dir, 'Rootnode.py'))
        directory_compare = filecmp.dircmp(test_dir, gen_dir)
        self.assertEqual(directory_compare.right_only, [])
        self.assertEqual(directory_compare.left_only, ['Rootnode.py'])


    def test_make_annotated_tree(self):
        evaluate.NUM_TRUE = -1
        xml_file = '../unit_test_classes_tags/Rootnode.xml'
        my_tree_object = evaluate.evaluate(xml_file)
        my_tree_output = extract._get_tree_output(my_tree_object.getroot())
        expected_output = "[0] Rootnode is true\n[1] Subnode1 is true\n[2] Subnode11 is true\n"
        self.assertEqual(my_tree_output, expected_output)
        # tree_output = extract._get_tree_exception_tb(my_tree_object.getroot())

    def test_write(self):
        evaluate.NUM_TRUE = -1
        xml_file = '../unit_test_classes_tags/Rootnode_missing_modules.xml'
        my_tree_object = evaluate.evaluate(xml_file)
        my_tree_object.write('/tmp/ewberg/tmp')
        get_xml_from_rootnode(my_tree_object.getroot())


    def test_make_annotated_tree_missing_module(self):
        evaluate.NUM_TRUE = -1
        xml_file = '../unit_test_classes_tags/Rootnode_missing_modules.xml'
        my_tree_object = evaluate.evaluate(xml_file)
        my_tree_output = extract._get_tree_output(my_tree_object.getroot())
        my_tree_exceptions = extract._get_tree_exceptions(my_tree_object.getroot())
        my_tree_exception_tb = extract._get_tree_exception_tb(my_tree_object.getroot())
        expected_output = "[0] Rootnode is true\n[1] Subnode1 is true\n[2] Subnode11 is true\n"
        expected_exceptions = "Subnode12: NotImplementedError\nSubnode13: ZeroDivisionError(\'division by zero\',)\nSubnode_none: No module named \'Subnode_none\'\nSubnode3: NotImplementedError\n"
        expected_exception_tb = "Subnode13: ['  File \"\S+ThenWhatTree/lib/twt_node/ThenWhatTreeNode.py\", line \d+, in evaluate_node_is_true\n    node_is_true = self.is_true()\n', '  File \"\S+Subnode13.py\", line \d+, in is_true\n    return 1/0\n']"
        self.assertEqual(my_tree_output, expected_output)
        self.assertEqual(my_tree_exceptions, expected_exceptions)
        self.assertRegex(my_tree_exception_tb, expected_exception_tb)


    def test_change_tag_to_name_attribute(self):
        import xml.etree.ElementTree as ET
        element = ET.Element('Reset')
        new_element = _standardize_tree_element(element)
        self.assertEqual(new_element.tag, 'node')
        self.assertEqual(new_element.find('name').text, 'Reset')

        element = ET.Element('Reset', name='Something')
        with self.assertRaises(ElementNameError):
            new_element = _standardize_tree_element(element)
        # self.assertEqual(new_element.tag, 'Reset')
        # self.assertEqual(new_element.find('name'), 'Something')

    def test_import_module_for_tree_element(self):
        evaluate._add_node_library_to_path('../unit_test_classes_tags')
        import xml.etree.ElementTree as ET
        element = ET.Element('node', name="Rootnode")
        evaluate._create_node_elements_from_xml_attrib(element)
        evaluate._import_module_for_tree_element(element)

        with self.assertRaises(ModuleNotFoundError):
            element = ET.Element('node', name='RRRootnode')
            evaluate._create_node_elements_from_xml_attrib(element)
            evaluate._import_module_for_tree_element(element)

    # def test_evaluate_tree_element(self):
    #     evaluate._add_node_library_to_path('../unit_test_classes_tags')
    #     import xml.etree.ElementTree as ET
    #     element = ET.Element('Rootnode')
    #     evaluate._evaluate_tree_element(element)
        # self.assertEqual(element.get('result'), {'node_is_true': 'true', 'output': 'Rootnode is 'true''})


    def test_add_branch_attrib(self):
        import xml.etree.ElementTree as ET
        element = ET.Element('test')
        evaluate.set_node_element(element, 'branch', 'my_name', 'Erik')
        evaluate.set_node_element(element, 'branch', 'time', 0)
        self.assertEqual(evaluate.get_node_element(element, 'branch', 'my_name'), 'Erik')
        self.assertEqual(evaluate.get_node_element(element, 'branch', 'time'), 0)

    def test_extract_functions(self):
        evaluate.NUM_TRUE = -1
        xml_file = '../unit_test_classes_branch_attrib/Rootnode_ma.xml'
        missing_attrib_tree_object = evaluate.evaluate(xml_file)
        missing_attrib_tree_text = extract._make_annotated_tree(missing_attrib_tree_object.getroot())
        missing_attrib_tree_output = extract._get_tree_output(missing_attrib_tree_object.getroot())
        missing_attrib_tree_exceptions = extract._get_tree_exceptions(missing_attrib_tree_object.getroot())
        expected_tree_text = "[0] zzRootnode_ma: true\n    [1] Subnode1_ma: true\n            Subnode11_ma: Exception raised\n        Subnode2_ma: Exception raised\n        Subnode3_ma: false\n        Subnode4_ma: Exception raised\n"
        expected_output = "[0] zzRootnode_ma is true\n[1] Subnode1_ma: Output override\n"
        expected_exceptions = "Subnode11_ma: \"Branch attribute: 'time' not assigned with 'set_branch_element' by any ancestor of Subnode11_ma\"\n"
        expected_exceptions += "Subnode2_ma: \"Branch attribute: 'time' not assigned with 'set_branch_element' by any ancestor of Subnode2_ma\"\n"
        expected_exceptions += "Subnode4_ma: \"XML attribute: 'test_xml_attr' not assigned for Subnode4_ma\"\n"
        self.assertEqual(missing_attrib_tree_output, expected_output)
        # self.assertEqual(missing_attrib_tree_text, expected_tree_text)
        # self.assertEqual(missing_attrib_tree_exceptions, expected_exceptions)

    def test_text_to_xml(self):
        self.maxDiff = None
        xml_string_pretty = '<?xml version="1.0" ?>\n' + \
                            '<node>\n' + \
                            '    <name>Rootnode</name>\n' + \
                            '    <node>\n' + \
                            '        <name>Subnode1</name>\n' + \
                            '        <node>\n' + \
                            '            <name>Subnode111</name>\n' + \
                            '        </node>\n' + \
                            '        <node>\n' + \
                            '            <name>Subnode12</name>\n' + \
                            '        </node>\n' + \
                            '        <node>\n' + \
                            '            <name>Subnode13</name>\n' + \
                            '        </node>\n' + \
                            '    </node>\n' + \
                            '    <node>\n' + \
                            '        <name>Subnode2</name>\n' + \
                            '    </node>\n' + \
                            '    <node>\n' + \
                            '        <name>Subnode3</name>\n' + \
                            '        <node>\n' + \
                            '            <name>Subnode31</name>\n' + \
                            '        </node>\n' + \
                            '        <node>\n' + \
                            '            <name>Subnode32</name>\n' + \
                            '        </node>\n' + \
                            '    </node>\n' + \
                            '</node>\n'

        element = text_to_xml('../unit_test_classes_tags/Rootnode.txt')
        self.assertEqual(element, xml_string_pretty)

    def test_add_elements(self):
        root = ET.Element('ThenWhatTree')
        my_element = ET.Element('node', attrib={'name':'Node1'})
        new_element = ET.Element('signal')
        new_element.text = '/soc_tb/soc'
        # append elements instead of using subelements
        my_element.append(new_element)
        root.append(my_element)
        second_element_node = ET.Element('node', attrib={'name':'Node11'})
        second_element = ET.Element('signal')
        second_element.text = '/soc_tb/soc/memss'
        second_element_node.append(second_element)
        my_element.append(second_element_node)
        for each_node in root.iter('node'):
            path = each_node.find('signal').text
        get_xml_from_rootnode(root)


    def test_csv_to_xml(self):
        element = csv_to_xml('../csv_files/csv_file')
        expected_output = '<?xml version="1.0" ?>\n' + \
                        '<node>\n' + \
                        '    <parent/>\n' + \
                        '    <name>Root</name>\n' + \
                        '    <stuff>A</stuff>\n' + \
                        '    <stuff1>B</stuff1>\n' + \
                        '    <node>\n' + \
                        '        <parent>Root</parent>\n' + \
                        '        <name>Subnode1</name>\n' + \
                        '        <stuff>1</stuff>\n' + \
                        '        <stuff1>2</stuff1>\n' + \
                        '        <node>\n' + \
                        '            <parent>Subnode1</parent>\n' + \
                        '            <name>Subnode11</name>\n' + \
                        '            <stuff>3</stuff>\n' + \
                        '            <stuff1>4</stuff1>\n' + \
                        '        </node>\n' + \
                        '    </node>\n' + \
                        '    <node>\n' + \
                        '        <parent>Root</parent>\n' + \
                        '        <name>Subnode2</name>\n' + \
                        '        <stuff/>\n' + \
                        '        <stuff1/>\n' + \
                        '        <node>\n' + \
                        '            <parent>Subnode2</parent>\n' + \
                        '            <name>Subnode21</name>\n' + \
                        '            <stuff>X</stuff>\n' + \
                        '            <stuff1>Y</stuff1>\n' + \
                        '        </node>\n' + \
                        '    </node>\n' + \
                        '</node>\n'
        self.assertEqual(expected_output, element)


    def test_csv_to_xml_missing_parent(self):
        with self.assertRaises(ParentNotFoundError):
            element = csv_to_xml('../csv_files/missing_parent.csv')

    def test_csv_to_xml_default_parent(self):
        element = csv_to_xml('../csv_files/default_parent.csv')
        expected_output = '<?xml version="1.0" ?>\n' + \
                        '<node>\n' + \
                        '    <name>node1</name>\n' + \
                        '    <parent/>\n' + \
                        '    <node>\n' + \
                        '        <name>node2</name>\n' + \
                        '        <parent/>\n' + \
                        '    </node>\n' + \
                        '</node>\n'
        self.assertEqual(expected_output, element)

    def test_get_fields_with_values(self):
        line0 = 'name,parent,other other'
        line1 = 'a b c,,x = 1'
        expected = {'name': 'a_b_c', 'parent': '', 'other_other': 'x = 1'}
        self.assertEqual(csv_to_xml_module._get_fields_with_values(line0, line1), expected)
        line0 = 'name,parent,other other'
        line1 = 'a b c,'
        with self.assertRaises(MissingDataEntries):
            csv_to_xml_module._get_fields_with_values(line0, line1)

    def test_check_names(self):
        my_dict = {'name': 'ab &c', 'notname': 'de f'}
        my_dict = csv_to_xml_module.remove_spaces_from_values(my_dict)
        self.assertEqual(my_dict, {'name': 'ab_&c', 'notname': 'de f'})
        with self.assertRaises(NonAlphaNumericCharacters):
            csv_to_xml_module.check_keys_for_bad_characters(my_dict)




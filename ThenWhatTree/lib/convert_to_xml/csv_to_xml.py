

# Copyright (C) 2018 Intel Corporation
# SPDX-License-Identifier: BSD-3-Clause

"""Module description here"""

# Import built in modules
import csv
import re

# Import 3rd party modules

# Import local modules
from ThenWhatTree.lib.convert_to_xml.common_functions import create_root_element, get_xml_from_rootnode, \
    create_subelement, add_subelements_to_node, _convert_text_file_to_list
from ThenWhatTree.lib.exceptions import ParentNotFoundError, NoParentGiven, MissingDataEntries, NonAlphaNumericCharacters

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
FIELDS_WITHOUT_SPACES = ['name', 'parent']


def csv_to_xml(csv_file):
    """

    :param csv_file:
    :return:
    """
    text_list = _convert_text_file_to_list(csv_file)
    rootnode = create_root_element()
    attributes = _get_fields_with_values(text_list[0], text_list[1])
    add_subelements_to_node(attributes, rootnode)
    last_element = rootnode
    for line in text_list[2:]:
        last_element = _add_subnode(rootnode, last_element, text_list[0], line)
    return get_xml_from_rootnode(rootnode)


def _add_subnode(rootnode, last_element, field_line, flow_line):
    attributes = _get_fields_with_values(field_line, flow_line)
    parent_element = find_parent_element(attributes, last_element, rootnode)
    subelement = create_subelement(parent_element, attributes)
    return subelement


def find_parent_element(attributes, last_element, rootnode):
    try:
        parent_element = _find_parent(rootnode, attributes['parent'])
    except KeyError:
        parent_element = last_element
    except NoParentGiven:
        parent_element = last_element
    return parent_element


def _find_parent(rootnode, parent_name):
    all_parents = convert_parent_name_to_list(parent_name)
    if len(all_parents) == 0:
        raise NoParentGiven
    for element in rootnode.iter('node'):
        element_has_name = element.find('name')
        if element_has_name is not None:
            if element_has_name.text in all_parents:
                all_parents.remove(element_has_name.text)
        if len(all_parents) == 0:
            return element
    raise ParentNotFoundError(','.join(all_parents))


def convert_parent_name_to_list(parent_name):
    all_parents = parent_name.split(',')
    new_parents = []
    for entry in all_parents:
        if len(entry.strip()) > 0:
            new_parents.append(entry)
    return [x.strip('"') for x in new_parents]


def _get_fields_with_values(fields, line):
    fields_list = get_fields_from_csv_string_remove_spaces(fields)
    values_list = get_fields_from_csv_string(line)
    if len(fields_list) > len(values_list):
        raise MissingDataEntries(fields, line)
    fields_dict = dict(zip(fields_list, values_list))
    fields_dict = remove_spaces_from_values(fields_dict)
    check_keys_for_bad_characters(fields_dict)
    return fields_dict

def check_keys_for_bad_characters(my_dict):
    for key in my_dict.keys():
        if key in FIELDS_WITHOUT_SPACES:
            if len(re.findall('\W', my_dict[key])) > 0:
                raise NonAlphaNumericCharacters(key, my_dict[key])


def remove_spaces_from_values(my_dict):
    for key in my_dict.keys():
        if key in FIELDS_WITHOUT_SPACES:
            my_dict[key] = my_dict[key].replace(' ', '_')
    return my_dict


def get_fields_from_csv_string_remove_spaces(csv_string):
    fields_list = [csv_string]
    fields_list = [x for x in csv.reader([x.replace(' ', '_') for x in fields_list])][0]
    return fields_list


def get_fields_from_csv_string(csv_string):
    fields_list = [csv_string]
    fields_list = [x for x in csv.reader(fields_list)][0]
    return fields_list

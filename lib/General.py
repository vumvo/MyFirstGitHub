__author__ = 'VUMVO'

import re
from robot.api import logger
from robot.libraries.BuiltIn import BuiltIn
from os import path
from lib import ExtendedExcelLibrary

""" General keywords """
# Define the scope of this Library, value can be: TEST CASE, TEST SUITE, GLOBAL
ROBOT_LIBRARY_SCOPE = 'GLOBAL'
# Specify the version of the Library
ROBOT_LIBRARY_VERSION = "0.1"


def compare_string(actual, expected):
    if expected[0] == '{' and expected[-1] == '}':
        logger.info("Compare between actual='" + actual +"' and expected='" + expected +"'")
        pattern = expected[1:-1]
        if re.search(pattern, actual):
            logger.info("Actual='" + actual +"' with pattern='" + pattern +"' is matched")
            return True
        else:
            return False
    else:
        return actual == expected


def get_absolute_path(file_path):
    execution_dir = BuiltIn().get_variables()
    execution_dir = execution_dir['${EXECDIR}']
    logger.info(execution_dir)
    absolute_path = path.join(execution_dir, file_path)
    logger.info(absolute_path)
    return absolute_path

def loading_variable_from_datatable(table_name, scope='TEST_SUITE'):
    excelLibraryInstance = BuiltIn().get_library_instance(table_name)
    variable_list = excelLibraryInstance.get_sheet_values()
    if scope=='TEST_SUITE':
        for row_value in range(1, len(variable_list)):
            BuiltIn().set_suite_variable(row_value[0], row_value[1])
    elif scope == 'TEST_CASE':
        for row_value in range(1, len(variable_list)):
            BuiltIn().set_test_variable(row_value[0], row_value[1])
    elif scope == 'GLOBAL':
        for row_value in range(1, len(variable_list)):
            BuiltIn().set_global_variable(row_value[0], row_value[1])

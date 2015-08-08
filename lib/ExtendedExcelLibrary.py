__author__ = 'VUMVO'

from ExcelLibrary import ExcelLibrary
from lib import General
from os import path
import os
from robot.api import logger

class ExtendedExcelLibrary(ExcelLibrary):

    ROBOT_LIBRARY_SCOPE = 'TEST SUITE'

    def __init__(self, file_name, sheetname=None, useTempDir=False):
        logger.info('Input: ' + file_name)
        logger.info(file_name[0])
        if file_name[0] == '/':
            _fileName = General.get_absolute_path(file_name[1:])
        else:
            _fileName = file_name
        logger.info(_fileName, False, True)

        self.wb = None
        self.tb = None
        self.sheetNum = None
        self.sheetNames = None
        self.fileName = None
        self.sheet = None
        if os.name is "nt":
            self.tmpDir = "Temp"
        else:
            self.tmpDir = "tmp"

        self.open_excel(_fileName, useTempDir)
        if sheetname:
            self.sheet = self.wb.sheet_by_index(self.sheetNames.index(sheetname))


    def get_cell_value_by_column_header(self,  row_index, header_name):
        column_header_index = self.get_column_header_index(header_name)
        return self.sheet.cell(row_index-1, column_header_index-1)

    def get_column_header_index(self, header_name):
        for col_index in range(self.sheet.ncols):
            value = self.sheet.cell(0, col_index).value
            if str(value) == header_name:
                return col_index + 1

    def get_row_values(self, row, includeEmptyCells=True):
        row_values = []
        for col_index in range(self.sheet.ncols):
            value = self.sheet.cell(int(row-1), col_index).value
            row_values.append(value)
        return row_values

    def get_sheet_values(self, includeEmptyCells=True):
        sheet_values = []
        for row_index in range(self.sheet.nrows):
            row_values = []
            for col_index in range(self.sheet.ncols):
                value = self.sheet.cell(row_index, col_index).value
                row_values.append(value)
            sheet_values.append(row_values)
        return sheet_values

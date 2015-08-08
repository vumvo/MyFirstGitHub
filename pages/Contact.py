'''
Created on Jun 13, 2015

@author: VUMVO
'''
from robot.libraries.BuiltIn import BuiltIn
from lib import General
from robot.api import logger
from selenium.webdriver.common.by import By
from Selenium2Library import Selenium2Library


class Contact(object):
    """
    High level action for Inbox page
    """

    def __init__(self):
        self._selenium2Library = BuiltIn().get_library_instance('selenium2Library')
        self.elements = {
                 'txtTemp' : '',
                'txtImportFile' : 'fName'
        }
    '''
    Usage: Import contact by uploading file.
    '''
    def import_contact_by_uploading_file(self, file_path):
        abs_path = General.get_absolute_path(file_path)
        self._selenium2Library.choose_file(self.elements['txtImportFile'], abs_path)
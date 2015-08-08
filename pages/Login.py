'''
Created on May 24, 2015

@author: VUMVO
'''

from robot.libraries.BuiltIn import BuiltIn
from robot.api import logger as logger
from selenium.webdriver.remote.webelement import WebElement


class Login(object):
    def __init__(self):
        # self._seleniumLib = BuiltIn().get_library_instance("lib.ExtendedSelenium2Library")
        self._selenium2Library = BuiltIn().get_library_instance("selenium2Library")

        # _title = self._seleniumLib.get_title()
        # logger.info("Working on page: %s" % (_title))
        self.elements = {
            'txtUsername': 'username',
            'txtPassword': 'passwd',
            'chkKeepMeSignedIn': 'persistent',
            'btnSignIn': 'login-signin',
            'formLogin': 'mbr-login-form',
            'lblLoginError': 'mbr-login-error',
            'txtTemp': ''

        }
    # def open_home_page(self):
    #     self._selenium2Library.open_browser("http://mail.yahoo.com")

    def login_with_valid_credential(self, username, password, is_keep_me_signed_in):
        self._selenium2Library.wait_until_number_of_windows(1, float(self._selenium2Library.timeout))

        element = self._selenium2Library.element_find(self.elements['txtUsername'], True, False, None)
        self._selenium2Library.wait_until_element_is_clickable(element, self._selenium2Library.timeout)
        self._selenium2Library.wait_until_element_is_clickable(self.elements['txtUsername'], self._selenium2Library.timeout)
        self._selenium2Library.wait_until_element_is_displayed(element, self._selenium2Library.timeout)
        # self._selenium2Library.wait_until_element_is_displayed(element, 10)
        self._selenium2Library.input_text(self.elements['txtUsername'], username)
        self._selenium2Library.input_password(self.elements['txtPassword'], password)
        if is_keep_me_signed_in:
            self._selenium2Library.select_checkbox(self.elements['chkKeepMeSignedIn'])
        elif not is_keep_me_signed_in:
            self._selenium2Library.unselect_checkbox(self.elements['chkKeepMeSignedIn'])
        self._selenium2Library.submit_form(self.elements['formLogin'])
        self._selenium2Library.wait_until_page_load(self._selenium2Library.timeout)

    def login_with_invalid_credential(self, username, password, is_keep_me_signed_in, error_message):
        self._selenium2Library.wait_until_number_of_windows(1, self._selenium2Library.timeout)

        element = self._selenium2Library.element_find(self.elements['txtUsername'], True, False, None)
        self._selenium2Library.wait_until_element_is_displayed(element, self._selenium2Library.timeout)
        self._selenium2Library.input_text(self.elements['txtUsername'], username)
        self._selenium2Library.input_password(self.elements['txtPassword'], password)
        if is_keep_me_signed_in:
            self._selenium2Library.select_checkbox(self.elements['chkKeepMeSignedIn'])
        elif not is_keep_me_signed_in:
            self._selenium2Library.unselect_checkbox(self.elements['chkKeepMeSignedIn'])
        self._selenium2Library.submit_form(self.elements['formLogin'])
        self._selenium2Library.wait_until_element_is_visible(self.elements['lblLoginError'],
                                                             self._selenium2Library.timeout)
        self._selenium2Library.element_text_should_be(self.elements['lblLoginError'], error_message)

    def verify_login_information(self, username, password, is_keep_me_signed_in):
        self._selenium2Library.textfield_value_should_be(self.elements['txtUsername'], username)
        if is_keep_me_signed_in:
            self._selenium2Library.checkbox_should_be_selected(self.elements['chkKeepMeSignedIn'])
        elif not is_keep_me_signed_in:
            self._selenium2Library.checkbox_should_not_be_selected(self.elements['chkKeepMeSignedIn'])

'''
Created on Jun 13, 2015

@author: VUMVO
'''
from robot.libraries.BuiltIn import BuiltIn
from robot.api import logger
from selenium.webdriver.common.by import By
from Selenium2Library import Selenium2Library
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC



class Inbox(object):
    """
    High level action for Inbox page
    """

    def __init__(self):
        self._selenium2Library = BuiltIn().get_library_instance('selenium2Library')
        self.elements = {
                 'txtTemp' : '',
                'mail_rows' : 'css=div[class^="list-view-item-container ml-bg"]',
                'mail_table' : 'msg-list',
                'btn_popup_category' : 'btn-select-dd',
                'btn_compose' : "css=button[data-action='compose']",
                'txt_to_field' : 'to-field',
                'txt_cc_field' : 'cc-field',
                'txt_bcc_field' : 'bcc-field',
                'txt_subject_field' : 'subject-field',
                'txt_body_field' : 'rtetext',
                'btn_send' : "css=span[data-action='send']",
                'lbl_from' : "css=div.thread-item-header span[aria-label*='from ']",
                'txt_mail_content' : 'css=div.email-wrapped',
                'btn_delete' : 'btn-delete'

        }
    '''
    Usage: Select the email based on row index. 1st-based index.
    '''
    def select_email_by_index(self, row_index = 1):
        locator = self.elements['mail_rows']
        rows = self._selenium2Library.element_find(locator, False, False, None)
        chk_select = rows[int(row_index)-1].find_element(By.CSS_SELECTOR, "input[role='checkbox']" )
        if not chk_select.is_selected():
            chk_select.click()

    '''
    Usage: Select mass emails whose sender is matched with the sender_name
    Note: This keyword couldn't select the all the emails if there are too many.
    '''
    def select_email_by_sender(self, sender_name):
        locator = self.elements['mail_rows']
        my_rows = self._selenium2Library.element_find(locator, False, False, None)
        logger.info(str(len(my_rows)))
        length = len(my_rows)
        print my_rows
        for i in range(len(my_rows)):
            # BuiltIn().sleep(1, "New Row----")
            # logger.info("Row: " + str(i))
            # logger.info(str(len(my_rows)))
            row = my_rows[i]
            # logger.info(str(row))
            self._selenium2Library.wait_until_element_is_displayed(row, self._selenium2Library.timeout)
            element_sender = row.find_element(By.XPATH, ".//div[starts-with(@class,'from')]")
            # logger.info("Found element_sender.")
            self._selenium2Library.wait_until_element_is_displayed(element_sender,
                                                                   self._selenium2Library.timeout)
            # logger.info("Is Sender element displayed? " + str(element_sender.is_displayed()))
            current_sender_name = element_sender.text.strip()
            # logger.info("Current Sender Name: " + current_sender_name)
            if current_sender_name == sender_name:
                # logger.info("Found matched")
                chk_select = row.find_element(By.XPATH, ".//input[@role='checkbox']")
                if not chk_select.is_selected():
                    chk_select.click()
            # Refresh the rows list
            my_rows = self._selenium2Library.element_find(locator, False, False, None)

    '''
    Usage: Select the 1st email whose title is matched with the input.
    '''
    def select_email_by_subject(self, subject):
        locator = self.elements['mail_table']

        email_table = self._selenium2Library.element_find(locator, True, False, None)
        # Find the checkbox which subject is match with the given subject
        xpath_locator = ".//span[normalize-space(@title)='" + subject + "']/ancestor::div[3]//input"
        checkboxes = email_table.find_elements(By.XPATH, xpath_locator)
        for chk_select in checkboxes:
            if not chk_select.is_selected():
                    chk_select.click()

    '''
    Usage: Open email by subject
    '''
    def open_email_by_subject(self, subject):
        locator = self.elements['mail_table']

        email_table = self._selenium2Library.element_find(locator, True, False, None)
        # Find the checkbox which subject is match with the given subject
        xpath_locator = ".//span[normalize-space(@title)='" + subject + "']"
        _element = email_table.find_element(By.XPATH, xpath_locator)
        _element.click()
        self._selenium2Library.wait_until_page_load(self._selenium2Library.timeout)

    '''
    Usage: Select the email by pre-define category
    Params:
        category: All, None, Read, Unread, Starred, Unstarred
    '''
    def select_email_by_category(self, category):
        self._selenium2Library.click_element(self.elements['btn_popup_category'])
        xpath_locator = "xpath=//div[@id='menu-ml-cbox']//span[text()='" + category + "']"
        self._selenium2Library.wait_until_element_is_visible(xpath_locator,
                                                             self._selenium2Library.timeout)
        button = self._selenium2Library.element_find(xpath_locator, True, False, None)
        button.click()

        '''
    Usage: Select the email by pre-define category
    Params:
        category: All, None, Read, Unread, Starred, Unstarred
    '''

    '''
    Usage: Click to compose an email
    Params:

    '''
    def compose_email(self):
        self._selenium2Library.click_element(self.elements['btn_compose'])
        self._selenium2Library.wait_until_element_is_visible(self.elements['txt_to_field'])

    '''
    Usage: Add recipient
    Params:
        to: list of to recipients, separated by ;
        cc: list of cc recipients, separeted by ;
        bcc: list of bcc recipients, separated by ;
    '''
    def _input_recipient(self, locator, text):
        for item in text.split(";"):
            input_text = item.split("|")
            if len(input_text)==1:
                self._selenium2Library.input_text(locator, input_text, False)
                self._selenium2Library.input_text(locator, Keys.TAB, False)
            else:
                self._selenium2Library.input_text(locator, input_text[0], False)
                text_holder = "xpath=//div[contains(.,'" + input_text[1] +"')]"
                self._selenium2Library.wait_until_element_is_displayed(text_holder, self._selenium2Library.timeout)
                #self._selenium2Library.delay(1)
                self._selenium2Library.click_element(text_holder)

    def add_recipients(self, to=None, cc=None, bcc=None):
        list_fields = [to, cc, bcc]
        list_locators = [self.elements['txt_to_field'], self.elements['txt_cc_field'], self.elements['txt_bcc_field']]
        for i in range(len(list_fields)):
            if list_fields[i]:
                self._input_recipient(list_locators[i], list_fields[i])

    def add_content(self, subject, body, override=True):
        if subject:
            self._selenium2Library.input_text(self.elements['txt_subject_field'], subject, override)
        if body:
            self._selenium2Library.input_text(self.elements['txt_body_field'], body, override)

    '''
    Usage: Click Send button to send email
    Params:
    '''
    def send_email(self):
        self._selenium2Library.click_element(self.elements['btn_send'])

    def verify_email_content(self, from_recipient=None, content=None):
        if from_recipient:
            self._selenium2Library.element_text_should_be(self.elements['lbl_from'], from_recipient.strip())
        if content:
            self._selenium2Library.element_text_should_be(self.elements['txt_mail_content'], content.strip())

    '''
    Usage: Delete the selected email
    '''
    def delete_selected_email(self):
        self._selenium2Library.click_element(self.elements['btn_delete'])

        '''
    Usage: Open email by subject
    '''
    def refresh_page_until_email_by_subject_exist(self, subject, timeout):
        # locator = self.elements['mail_table']
        # email_table = self._selenium2Library.element_find(locator, True, False, None)
        # Find the checkbox which subject is match with the given subject
        logger.info(subject, True, True)
        xpath_property = "xpath=//span[normalize-space(@title)='" + subject + "']"
        self._selenium2Library.reload_page_until_element_displayed(xpath_property, timeout)
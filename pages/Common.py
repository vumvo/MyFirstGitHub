'''
Created on May 24, 2015

@author: VUMVO
'''

from robot.libraries.BuiltIn import BuiltIn
from robot.api import logger as logger

class Common(object):

    def __init__(self):
        # self._seleniumLib = BuiltIn().get_library_instance("lib.ExtendedSelenium2Library")
        self._selenium2Library = BuiltIn().get_library_instance("selenium2Library")

        # _title = self._seleniumLib.get_title()
        # logger.info("Working on page: %s" % (_title))
        self.elements = {
                 'btnLogout' : "yucs-signout",
                 'lblProfile' : "xpath=//a[@aria-label='Profile']",
                 'treeNavigation' : 'storm-listnav',
                 'btnSignIn' : 'login-signin',
                 'formLogin' : 'mbr-login-form',
                 'btnEmptyTrash' : 'btn-emptytrash',
                'btnEmptySpam' : 'btn-emptyspam',
                'btnConfirmOK': 'okayModalOverlay',
                'btnConfirmCancel': 'cancelModalOverlay',
                 'txtTemp' : ''
        }

    '''
    Usage: Log out
    '''
    def logout(self):
        self._selenium2Library.javascript_click(self.elements['lblProfile'], 'click')
        self._selenium2Library.wait_until_element_is_visible(self.elements['btnLogout'], 20)
        self._selenium2Library.click_element(self.elements['btnLogout'])
        #self._selenium2Library.click_element(self.elements['btnLogout'])
        self._selenium2Library.wait_until_page_load(self._selenium2Library.timeout)

    '''
    Usage: Select a node on the Navigation tree
    '''
    def select_navigation_node(self, node_name):
        # locator = 'xpath=//a[contains(@title,"' + node_name + '")]'
        # ul#storm-listnav a[title^='Sent']
        locator = "css=ul#storm-listnav a[title^='" + node_name + "']"
        locator = "xpath=//*[@id='storm-listnav']//*[starts-with(.,'"+ node_name + "')]"
        self._selenium2Library.click_element(locator)
        self._selenium2Library.wait_until_page_load(self._selenium2Library.timeout)

    '''
    Usage: Select a menu item on the master menu (most top horizontal navigation)
    '''
    def select_master_menu_item(self, menu_item):
        locator = 'xpath=//a[contains(text(),"' + menu_item + '")]'
        # The following css locators don't work. Don't know why :(
        # masterNav [id$=news]
        # locator = "css=#masterNav [id~=" + menu_item.lower() + "]"
        # locator = "css=#yucs-top-" + menu_item.lower()
        self._selenium2Library.click_link(locator)
        self._selenium2Library.wait_until_page_load(self._selenium2Library.timeout)

    '''
    Usage: Click button on the Yahoo Mail toolbar button.
    '''
    def click_toolbar_item(self, item_name):
        # Example: li[title=Mail]
        locator = 'css=li[title='+item_name+']'
        self._selenium2Library.click_element(locator)
        self._selenium2Library.wait_until_page_load(self._selenium2Library.timeout)

    '''
    Usage: Empty the Trash folder
    '''
    def empty_trash(self, confirm = True):
        locator = "css=ul#storm-listnav a[title^='Trash']"
        self._selenium2Library.mouse_over(locator)
        self._selenium2Library.wait_until_element_is_visible(self.elements['btnEmptyTrash'], 10)
        self._selenium2Library.click_element(self.elements['btnEmptyTrash'])
        if bool(confirm):
            self._selenium2Library.click_element(self.elements['btnConfirmOK'])
        else:
            self._selenium2Library.click_element(self.elements['btnConfirmCancel'])

    '''
    Usage: Empty the Spam folder
    '''
    def empty_spam(self, confirm=True):
        locator = "css=ul#storm-listnav a[title^='Spam']"
        self._selenium2Library.mouse_over(locator)
        self._selenium2Library.wait_until_element_is_visible(self.elements['btnEmptySpam'], 10)
        self._selenium2Library.click_element(self.elements['btnEmptySpam'])
        logger.info(confirm)
        if bool(confirm):
            self._selenium2Library.click_element(self.elements['btnConfirmOK'])
        else:
            self._selenium2Library.click_element(self.elements['btnConfirmCancel'])



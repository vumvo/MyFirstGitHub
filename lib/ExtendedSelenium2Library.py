'''
Created on Jun 13, 2015

@author: VUMVO
'''
from Selenium2Library import Selenium2Library
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from robot.api import logger
from lib import General as general
from selenium.webdriver.common import action_chains


# Limit the methods to be used as keywords by __all__ attribute
# __all__ = ['example_keyword', 'second_example']


class ExtendedSelenium2Library(Selenium2Library):
    """ Extended Selenium2Library """
    # Define the scope of this Library, value can be: TEST CASE, TEST SUITE, GLOBAL
    ROBOT_LIBRARY_SCOPE = 'GLOBAL'
    # Specify the version of the Library
    ROBOT_LIBRARY_VERSION = "0.1"

    # def __init__(self):
    # self.implicit_timeout = self.get_selenium_implicit_wait()
    # self.timeout = self.get_selenium_timeout()
    # self.speed = self.get_selenium_speed()

    @property
    def implicit_timeout(self):
        return self._implicit_wait_in_secs

    @property
    def timeout(self):
        return self._timeout_in_secs

    @property
    def selenium_speed(self):
        return self._speed_in_secs

    # example
    def hello(self, name):
        print "Hello, %s" % name
        logger.info("Hello Extended Selenium2Library")

    # Page

    def get_web_driver_instance(self):
        return  self._current_browser()

    def select_window_title(self, title, timeout, index=1):
        """Selects the window found with `locator` as the context of actions.

        If the window is found, all subsequent commands use that window, until
        this keyword is used again. If the window is not found, this keyword fails.

        By default, when a locator value is provided,
        it is matched against the title of the window and the
        javascript name of the window. If multiple windows with
        same identifier are found, the first one is selected.

        Special locator `main` (default) can be used to select the main window.

        It is also possible to specify the approach Selenium2Library should take
        to find a window by specifying a locator strategy:

        | *Strategy* | *Example*                               | *Description*                        |
        | title      | Select Window `|` title=My Document     | Matches by window title              |
        | name       | Select Window `|` name=${name}          | Matches by window javascript name    |
        | url        | Select Window `|` url=http://google.com | Matches by window's current URL      |

        Example:
        | Click Link | popup_link | # opens new window |
        | Select Window | popupName |
        | Title Should Be | Popup Title |
        | Select Window |  | | # Chooses the main window again |
        """

        def wait_for_window_title(browser):
            _index = index
            _browser = self._current_browser()
            for handle in _browser.get_window_handles():
                _browser.switch_to_window(handle)
                logger.info(self.get_title())
                if general.compare_string(self.get_title().strip().lower(), title.lower()):
                    _index = int(_index) - 1
                    logger.info("Switched to window title '" + browser.get_title() + "'")
                    if _index == 0:
                        return True

        wait = WebDriverWait(self._current_browser(), float(timeout))
        wait.until(wait_for_window_title, "Error: Could not wait until window title '" + title + "' display")

    '''
    Usage: wait for state of the document is complete (javascript)
    '''
    def wait_until_page_load(self, timeout):
        self.wait_for_condition(""
                                "if (document.readyState == 'complete')"
                                " return true;"
                                "else "
                                "return false;"
                                , timeout)

    '''
    Usage: Wait until an element is no visible
    '''
    def wait_until_element_is_not_visible(self, locator, timeout, error):
        def check_visibility():
            visible = not self._is_visible(locator)
            if visible:
                return
            elif visible is None:
                return error or "Element locator '%s' did not match any elements after %s" % (
                    locator, self._format_timeout(timeout))
            else:
                return error or "Element '%s' was not visible in %s" % (locator, self._format_timeout(timeout))

        self._wait_until_no_error(timeout, check_visibility)

    '''
    Usage: wait until alert is present
    '''
    def wait_until_alert_display(self, timeout):
        WebDriverWait(self._current_browser(), timeout).until(
            EC.alert_is_present()
        )
    '''
    Usage: verify title should start with
    '''
    def title_should_start_with(self, expect):
        title = self.get_title()
        if not title.startswith(expect):
            raise AssertionError("Title '%s' did not start with '%s'." % (title, expect))

    '''
    Usage: verify title should contains
    '''
    def title_should_contains(self, title):
        """Verifies that current page title contains `title`."""
        actual = self.get_title()
        if title not in actual:
            raise AssertionError("Title should contain '%s' but it doesn't. It's is '%s'"
                                 % (title, actual))
        self._info("Page title is '%s'." % title)

    # Element keywords

    def element_attribute_should_be(self, attribute_locator, attribute_value):
        value = self.get_element_attribute(attribute_locator)
        if not value == attribute_value:
            raise AssertionError("Attribute '%s' is not equal to '%s', actual value is '%s'."
                                 % (attribute_locator, attribute_value, value))

    def element_attribute_should_not_be(self, attribute_locator, attribute_value):
        value = self.get_element_attribute(attribute_locator)
        if value == attribute_value:
            raise AssertionError("Attribute '%s' is equal to '%s'. It should be not."
                                 % (attribute_locator, attribute_value))

    def javascript_click(self, locator, click_type='click'):
        element = self._element_find(locator, True, False, None)
        self._click_on_element(element, click_type, True)

    # Table keywords

    def click_table_cell(self, table_locator, row_index, column_index, click_type='click'):
        table = self._table_element_finder(table_locator)
        cell = table.find_elements_by_xpath('./descendant::tr[' + row_index + ']/td[' + column_index + ']')
        self._click_on_element(cell, click_type, False)

    # Wait Keywords

    def wait_for_window_title_display(self, windowTitle, timeout=None, error=None):
        if not error:
            error = "Window title '%s' did not display in <TIMEOUT>" % windowTitle
        self._wait_until(timeout, error,
                         lambda: self._window_manager.get_window_titles(self._current_browser()).count(windowTitle) > 0)

    def wait_for_element_attribute_value(self, attribute_locator, attribute_value, timeout=None, error=None):
        if not error:
            error = "Attribute '%s' did not change to expected value in <TIMEOUT>" % attribute_locator, attribute_value
        self._wait_until(timeout, error,
                         lambda: self.get_element_attribute(attribute_locator).strip() == attribute_value.strip())

    def wait_for_clickable(self, locator, timeout=None, error=None):
        element = self._element_find(locator, True, False, None)
        self._wait_until(timeout, error, element.is_display() and element.is_enabled())
        # WebDriverWait(self._current_browser(), timeout).until(EC.element_to_be_clickable(element))

    def element_find(self, locator, first_only=True, required=False, tag=None):
        return self._element_find(locator, first_only, required, tag)

    def get_web_driver(self):
        return self._current_browser()

    def wait_until_number_of_windows(self, number_of_windows, timeout):
        WebDriverWait(self._current_browser(), timeout).until(
            lambda s: len(s.window_handles) == number_of_windows
        )

    def wait_until_element_is_displayed(self, locator, timeout):
        logger.info('Wait until element is displayed....')
        _element = self._element_find(locator, True, False, None)
        wait = WebDriverWait(_element, timeout)
        wait.until(lambda s: s.is_displayed())
        logger.info('Finish waiting')

    def wait_until_element_is_clickable(self, locator, timeout):
        logger.info('Wait until element is clickable...')
        _element = self._element_find(locator, True, True, None)
        wait = WebDriverWait(_element, timeout)
        wait.until(
            lambda s: s.is_enabled() and s.is_displayed()
        )

    # ******* Private
    def _click_on_element(self, element, click_type='click', use_javascript=False):
        if not use_javascript:
            if click_type == 'click':
                element.click()
            elif click_type == 'double_click':
                element.double_click()
            elif click_type == 'context_click':
                element.context_click()
        else:
            self._current_browser().execute_script("arguments[0].click();", element)

    # ****** Override method
    def _element_find(self, locator, first_only, required, tag=None):
        logger.info('Using override _element_find method')
        if not isinstance(locator, WebElement):
            return super(ExtendedSelenium2Library, self)._element_find(locator, first_only, required, tag)
        else:
            return locator

    def input_text(self, locator, text, override=True):
        if locator:
            element = self._element_find(locator, True, True)
            if override:
                element.clear()
            element.send_keys(text)
        else:
            action_chains(self._current_browser()).send_keys(text).perform()

    def reload_page_until_element_displayed(self, locator, timeout):
        def reload_page_and_find_element():
            self.reload_page()
            logger.info('Reload Page')
            return self.element_find(locator, True, False, None) != None

        self._wait_until(timeout, "Locator '" + locator + " is not displayed after timeout '" + str(timeout) + "'",
                         reload_page_and_find_element)

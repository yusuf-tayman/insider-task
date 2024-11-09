from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class Base(object):
    """
    Base class to initialize the base page that will be called from all pages
    """

    def __init__(self, driver, explicit_wait=50):
        """
        Init method for Base class
        :param driver: WebDriver instance
        :param explicit_wait: int - time to wait for element to be visible

        """
        self.driver = driver
        self.wait = WebDriverWait(self.driver, explicit_wait)

    def driver(self):
        return self.driver

    def get_element(self, locator):
        """
        Get element by locator
        :param locator:
        :return:
        """
        return self.driver.find_element(*locator)

    def wait_for_element(self, locator):
        """
        Wait for element to be clickable
        :param locator:
        :return:
        """
        return self.wait.until(EC.presence_of_element_located(locator))

    def is_element_visible(self, locator, message):
        """
        Check if element is visible
        :param message:
        :param locator:
        :return:
        """
        try:
            self.wait.until(EC.visibility_of_element_located(locator), message)
            return True
        except:
            return False

    def get_elements(self, locator):
        """
        Get elements by locator
        :param locator:
        :return:
        """
        return self.driver.find_elements(*locator)

    def quit_driver(self):
        """
        Quit driver

        """
        if self.driver is not None:
            self.driver.quit()

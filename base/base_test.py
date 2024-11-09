import logging
import os
import unittest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions


class BaseTest(unittest.TestCase):
    driver = None
    browser = None
    logger = None

    def setUp(self):
        """
        Sets up the test by initializing the driver and logger.

        """
        self.init_logger()
        self.init_driver()

    def init_driver(self):
        """
        Initialize the WebDriver based on browser choice

        """
        if self.browser == "chrome":
            chrome_options = ChromeOptions()
            chrome_options.add_argument("--headless")
            self.driver = webdriver.Chrome(options=chrome_options)
        elif self.browser == "firefox":
            firefox_options = FirefoxOptions()
            firefox_options.add_argument("--headless")
            self.driver = webdriver.Firefox(options=firefox_options)
        else:
            raise ValueError(f"Browser '{self.browser}' is not supported")

        self.driver.maximize_window()

    def init_logger(self):
        """
        Sets up a logger for each test case.

        """
        logger = logging.getLogger(self.__class__.__name__)
        logger.setLevel(logging.INFO)
        handler = logging.StreamHandler()
        handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
        logger.addHandler(handler)
        self.logger = logger

    def take_screenshot(self):
        """
        Capture a screenshot when a test fails

        """
        screenshot_dir = "screenshots"
        if not os.path.exists(screenshot_dir):
            os.makedirs(screenshot_dir)

        screenshot_path = os.path.join(screenshot_dir, f"{self._testMethodName}_failure.png")
        self.driver.save_screenshot(screenshot_path)
        self.logger.error(f"Test failed. Screenshot saved to {screenshot_path}")

    def tearDown(self):
        """
        Takes a screenshot if a test fails and cleans up after each test.

        """
        if self._outcome.errors:
            for test, err in self._outcome.errors:
                if err:
                    self.take_screenshot()

        if self.driver:
            self.driver.quit()


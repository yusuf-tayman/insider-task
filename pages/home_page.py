from selenium.webdriver.common.by import By
from base.page_base import PageBase


class HomePage(PageBase):
    COMPANY_MENU = (By.LINK_TEXT, "Company")
    CAREERS_LINK = (By.LINK_TEXT, "Careers")
    COOKIE_ACCEPT = (By.XPATH, "//a[@id='wt-cli-accept-all-btn']")

    def __init__(self, driver):
        super().__init__(driver)

        self.check()

    def check(self):
        self.is_element_visible(self.COMPANY_MENU, 'Company menu is not visible!')

    def go_to_careers(self):
        """
        Clicks on Company -> Careers link

        """
        self.wait_for_element(self.COOKIE_ACCEPT).click()
        self.wait_for_element(self.COMPANY_MENU).click()
        self.wait_for_element(self.CAREERS_LINK).click()

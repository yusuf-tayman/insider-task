from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec

from base.page_base import PageBase


class CareersPage(PageBase):
    TEAMS_SECTION = (By.XPATH, "//div[@data-id='b6c45b2']")
    LOCATIONS_SLIDER = (By.XPATH, "//div[@data-id='38b8000']")
    LIFE_SECTION = (By.XPATH, "//section[@data-id='a8e7b90']")
    QA_JOBS_LINK = (By.LINK_TEXT, "See all QA jobs")

    def __init__(self, driver):
        super().__init__(driver)
        self.check()

    def check(self):
        assert self.is_element_visible(self.LOCATIONS_SLIDER, "Locations block is not visible!")
        assert self.is_element_visible(self.TEAMS_SECTION, "Teams block is not visible!")
        assert self.is_element_visible(self.LIFE_SECTION, "Life at Insider block is not visible!")

    def go_to_qa_jobs(self):
        """
        Navigate to the Quality Assurance job listings.

        """
        self.driver.get("https://useinsider.com/careers/quality-assurance/")

        self.wait.until(ec.element_to_be_clickable(self.QA_JOBS_LINK)).click()

from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec

from base.page_base import PageBase


class JobsPage(PageBase):
    JOBS_LIST_CONTAINER = (By.ID, "jobs-list")
    JOB_ITEM = (By.CLASS_NAME, "position-list-item")
    JOB_ITEMS = (By.CLASS_NAME, "position-list-item-wrapper")
    POSITION_TITLE = (By.CLASS_NAME, "position-title")
    POSITION_DEPARTMENT = (By.CLASS_NAME, "position-department")
    POSITION_LOCATION = (By.CLASS_NAME, "position-location")
    VIEW_ROLE_BUTTON = (By.LINK_TEXT, "View Role")
    LOCATION_FILTER_DROPDOWN = (By.ID, "filter-by-location")
    DEPARTMENT_FILTER_DROPDOWN = (By.ID, "filter-by-department")
    LOCATION_OPTIONS = (By.CSS_SELECTOR, '#filter-by-location option')
    DEPARTMENT_OPTIONS = (By.CSS_SELECTOR, '#filter-by-department option')

    def __init__(self, driver):
        super().__init__(driver)
        self.check()

    def check(self):
        self.is_element_visible(self.LOCATION_FILTER_DROPDOWN, "Locations block is not visible!")
        self.is_element_visible(self.DEPARTMENT_FILTER_DROPDOWN, "Teams block is not visible!")
        self.is_element_visible(self.JOBS_LIST_CONTAINER, "Life at Insider block is not visible!")

    def wait_until_job_list_refreshed(self, new_location):
        """
        Wait until the job list has been refreshed based on the updated data-location attribute.
        :param new_location: New location to wait for

        """

        self.wait.until(ec.presence_of_all_elements_located(self.JOB_ITEM))
        self.wait.until(ec.visibility_of_all_elements_located(self.JOB_ITEM))

        job_items = self.driver.find_elements(*self.JOB_ITEM)

        current_locations = [job.get_attribute('data-location') for job in job_items]

        self.wait.until(lambda driver: any(location == new_location for location in current_locations))

    def apply_location_filter(self, location):
        """
        Apply the location filter and wait for the job list to be refreshed.
        :param: location: Location to filter by

        """

        self.wait.until(ec.visibility_of_all_elements_located(self.LOCATION_OPTIONS))

        location_option = self.wait.until(
            ec.presence_of_element_located((By.XPATH, f"//option[contains(text(), '{location.strip()}')]"))
        )
        location_option.click()

        normalized_location = location.strip().replace(" ", "-").replace(",", "").lower()

        self.wait.until(lambda driver: all(
            job.get_attribute("data-location") == normalized_location
            for job in driver.find_elements(*self.JOB_ITEM)
        ))

    def apply_department_filter(self, department):
        """
        Apply the department filter and wait for the job list to be refreshed.
        :param: department: Department to filter by
        """
        department_dropdown_element = self.wait_for_element(self.DEPARTMENT_FILTER_DROPDOWN)
        self.wait.until(ec.visibility_of_all_elements_located(self.DEPARTMENT_OPTIONS))

        department_dropdown = Select(department_dropdown_element)
        department_dropdown.select_by_visible_text(department)

        self.wait.until(lambda driver: all(
            job.is_displayed() for job in driver.find_elements(*self.JOB_ITEM)
        ))

    def apply_filters(self, location, department):
        """
        Apply the location and department filters.
        :param location: Location to filter by
        :param department: Department to filter by

        """
        self.apply_location_filter(location)
        self.apply_department_filter(department)

    def get_jobs(self):
        """
        Retrieve all job items listed on the page.

        """
        self.wait.until(ec.presence_of_element_located(self.JOBS_LIST_CONTAINER))
        jobs_container = self.wait_for_element(self.JOBS_LIST_CONTAINER)
        return jobs_container.find_elements(*self.JOB_ITEM)

    def get_job_details(self, job):
        """
        Retrieve job title, department, and location details for assertions.
        :param job: Job item element

        """
        position_title = job.find_element(*self.POSITION_TITLE).text
        department = job.find_element(*self.POSITION_DEPARTMENT).text
        location = job.find_element(*self.POSITION_LOCATION).text
        return position_title, department, location

    def click_view_role(self):
        """
        Hover over a job item and click 'View Role'.

        """
        job_items = WebDriverWait(self.driver, 10).until(
            ec.presence_of_all_elements_located(self.JOB_ITEMS)
        )
        job_item = job_items[0]
        actions = ActionChains(self.driver)
        actions.move_to_element(job_item).perform()
        view_role_button = job_item.find_element(By.LINK_TEXT, "View Role")
        actions.move_to_element(view_role_button).perform()
        view_role_button.click()

    def is_application_form_opened(self):
        """
        Verifies the application form opened in Lever.

        """
        window_handles = self.driver.window_handles
        self.driver.switch_to.window(window_handles[1])
        return "lever.co/useinsider" in self.driver.current_url

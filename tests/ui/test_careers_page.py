import pytest
from base.base_test import BaseTest
from pages.home_page import HomePage
from pages.careers_page import CareersPage
from pages.jobs_page import JobsPage


class TestCareersPage(BaseTest):

    @pytest.fixture(autouse=True)
    def setup(self, browser):
        """Setup WebDriver based on the browser passed via pytest fixture."""
        self.browser = browser
        super().setUp()
        self.location = "Istanbul, Turkey"
        self.department = "Quality Assurance"

    """
    Test case is:
    1. Visit the Insider homepage.
    2. Navigate to the Careers page.
    3. Filter jobs for Quality Assurance in Istanbul.
    4. Apply job filters.
    5. Verify job filters.
    6. Check View Role link redirects to application form.
    
    """
    def test_careers_navigation_and_job_search(self):
        self.logger.info("Step 1: Visiting Insider homepage.")
        self.driver.get("https://useinsider.com/")
        home_page = HomePage(self.driver)
        self.logger.info("Step 2: Navigating to Careers page.")
        home_page.go_to_careers()
        careers_page = CareersPage(self.driver)

        self.logger.info("Step 3: Filtering jobs for Quality Assurance in Istanbul.")
        careers_page.go_to_qa_jobs()
        jobs_page = JobsPage(self.driver)

        self.logger.info("Step 4: Applying job filters.")
        jobs_page.apply_filters(self.location, self.department)

        self.logger.info("Step 5: Verifying job filters.")
        jobs = jobs_page.get_jobs()
        self.assertGreater(len(jobs), 0, "No jobs found for the specified criteria.")

        for job in jobs:
            position_title, department, location = jobs_page.get_job_details(job)
            self.assertIn("Quality Assurance", position_title, "Position title does not contain 'Quality Assurance'.")
            self.assertEqual(department, "Quality Assurance", "Job department is not 'Quality Assurance'.")
            self.assertEqual(location, "Istanbul, Turkey", "Job location is not 'Istanbul, Turkey'.")

        self.logger.info("Step 6: Checking View Role link redirects to application form.")
        jobs_page.click_view_role()
        self.assertTrue(jobs_page.is_application_form_opened(), "Application form did not open.")

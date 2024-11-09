from locust import HttpUser, task, between
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class N11User(HttpUser):
    host = "https://www.n11.com"

    wait_time = between(1, 3)

    @task
    def search_n11(self):
        logger.info("Starting search test")
        homepage_response = self.client.get("/")
        if homepage_response.status_code != 200:
            print("Failed to load homepage")
            return

        logger.info("Homepage loaded successfully")

        logger.info("Searching for a product")
        search_query = "laptop"
        search_response = self.client.get(f"/arama?q={search_query}")

        logger.info("Checking search results")
        if search_response.status_code == 200:
            print("Search results page loaded successfully")
        else:
            print("Search request failed")

        logger.info("Checking if search term is present in search results")
        if "laptop" in search_response.text.lower():
            print("Search results contain the search term.")
        else:
            print("Search term not found in results.")

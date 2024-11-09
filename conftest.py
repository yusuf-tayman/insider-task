import pytest
from faker import Faker

from api_client.pet_client import PetClient
from logger import logger


@pytest.fixture
def pet_client():
    """Fixture to provide an instance of PetClient."""
    return PetClient()


@pytest.fixture
def random_pet_data():
    """Fixture to generate random pet data."""
    faker = Faker()
    data = {
        "id": faker.random_int(min=100000, max=999999),
        "name": faker.first_name(),
        "status": faker.random_element(elements=("available", "pending", "sold"))
    }
    logger.info(f"Generated random pet data: {data}")
    return data


def pytest_addoption(parser):
    parser.addoption(
        "--browser", action="store", default="chrome", help="Choose browser: chrome or firefox"
    )


@pytest.fixture(scope="session")
def browser(request):
    return request.config.getoption("--browser")

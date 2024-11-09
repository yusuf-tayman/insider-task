import pytest
import random
from conftest import logger

BASE_URL = "https://petstore.swagger.io/v2"


class TestPetStoreAPI:

    @pytest.fixture
    def random_pet_data(self, faker):
        """
        Fixture to generate random pet data for testing.

        """
        data = {
            "id": faker.random_int(min=100000, max=999999),
            "name": faker.first_name(),
            "status": faker.random_element(elements=("available", "pending", "sold"))
        }
        logger.info(f"Generated random pet data: {data}")
        return data

    @pytest.fixture
    def pet_id(self, pet_client, random_pet_data):
        """
        Create a pet and return the pet's ID for use in subsequent tests.

        """
        response = pet_client.create_pet(random_pet_data)
        assert response.status_code == 200, "Failed to create pet"
        return random_pet_data["id"]

    @pytest.mark.parametrize(
        "status",
        ["available", "pending", "sold"]
    )
    def test_create_pet_with_different_valid_statuses(self, pet_client, status):
        """
        Positive test case for creating a pet with different statuses.

        """
        pet_data = {
            "id": random.randint(100000, 999999),
            "name": "TestPet",
            "status": status
        }
        response = pet_client.create_pet(pet_data)
        assert response.status_code == 200
        pet = response.json()
        assert pet["name"] == "TestPet"
        assert pet["status"] == status
        logger.info(f"Pet created with status {status}.")

    def test_create_pet_without_id(self, pet_client, random_pet_data):
        """
        Test creating a pet without providing an ID, and the server generates one.

        """
        pet_data = random_pet_data.copy()
        pet_data["id"] = None
        response = pet_client.create_pet(pet_data)
        assert response.status_code == 200
        pet = response.json()
        assert "id" in pet
        logger.info(f"Pet created with generated ID {pet['id']}.")

    def test_get_pet_by_id(self, pet_client, pet_id):
        """
        Test retrieving a pet by its ID.

        """
        pet = pet_client.get_pet(pet_id)
        assert pet is not None
        assert pet["id"] == pet_id
        logger.info(f"Successfully retrieved pet with ID {pet_id}.")

    def test_get_pet_with_unknown_id(self, pet_client):
        """
        Test retrieving a pet that doesn't exist.

        """
        invalid_pet_id = 9999999999
        response = pet_client.get_pet(invalid_pet_id)
        assert response is None
        logger.info(f"Attempted to retrieve pet with invalid ID {invalid_pet_id}.")

    def test_update_pet(self, pet_client, pet_id):
        """
        Test updating a pet's details (name and status).

        """
        updated_data = {
            "id": pet_id,
            "name": "Updated Pet",
            "status": "sold"
        }
        response = pet_client.update_pet(updated_data)
        assert response.status_code == 200
        pet = response.json()
        assert pet["name"] == "Updated Pet"
        assert pet["status"] == "sold"
        logger.info(f"Successfully updated pet with ID {pet_id}.")

    def test_update_pet_to_invalid_status(self, pet_client, pet_id):
        """
        Test attempting to update a pet with an invalid status.

        """
        invalid_data = {
            "id": pet_id,
            "name": "Invalid Pet",
            "status": "unknown_status"
        }
        response = pet_client.update_pet(invalid_data)
        assert response.status_code == 200
        logger.info(f"Attempted to update pet with invalid status.")

    def test_delete_pet(self, pet_client, pet_id):
        """
        Test deleting a pet by its ID.

        """
        response = pet_client.delete_pet(pet_id)
        assert response.status_code == 200
        logger.info(f"Successfully deleted pet with ID {pet_id}.")

        response = pet_client.get_pet(pet_id)
        assert response is None
        logger.info(f"Verified that pet with ID {pet_id} is deleted.")

    def test_find_pet_by_status(self, pet_client):
        """
        Test finding pets by their status.

        """
        response = pet_client.find_pet_by_status("sold")
        assert isinstance(response, list)
        for pet in response:
            assert pet["status"] == "sold"
        logger.info("Found pets with status 'sold'.")

    def test_find_pet_by_unknown_status(self, pet_client):
        """
        Test searching for pets with an unknown status.

        """
        response = pet_client.find_pet_by_status("notavailable")
        assert isinstance(response, list)
        assert len(response) == 0
        logger.info("Found no pets with unknown status 'notavailable'.")

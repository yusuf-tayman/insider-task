from .base_client import BaseAPIClient
import requests


class PetClient(BaseAPIClient):
    def create_pet(self, pet_data):
        url = f"{self.BASE_URL}/pet"
        return self._post(url, pet_data)

    def get_pet(self, pet_id):
        url = f"{self.BASE_URL}/pet/{pet_id}"
        try:
            return self._get(url)
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 404:
                return None
            raise

    def update_pet(self, pet_data):
        url = f"{self.BASE_URL}/pet"
        return self._put(url, pet_data)

    def delete_pet(self, pet_id):
        url = f"{self.BASE_URL}/pet/{pet_id}"
        return self._delete(url)

    def find_pet_by_status(self, status):
        """
        Find pets by their status.
        :param: status: The status of the pets to retrieve (e.g., 'sold', 'available', etc.)
        :return: List of pets with the given status
        """
        url = f"{self.BASE_URL}/pet/findByStatus"
        return self._get(url, params={"status": status})


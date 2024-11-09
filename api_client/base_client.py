import requests


class BaseAPIClient:
    BASE_URL = "https://petstore.swagger.io/v2"

    def __init__(self):
        self.headers = {"Content-Type": "application/json"}

    def _get(self, url, params=None):
        """
        Send a GET request to the specified URL.
        :param: url: URL to send the request to
        :param params: Query parameters
        :return:

        """
        response = requests.get(url, headers=self.headers, params=params)
        response.raise_for_status()
        return response.json()

    def _post(self, url, data):
        """
        Send a POST request to the specified URL.
        :param: url: URL to send the request to
        :param data: JSON data to send in the request body
        :return:

        """
        response = requests.post(url, json=data, headers=self.headers)
        response.raise_for_status()
        return response

    def _put(self, url, data):
        """
        Send a PUT request to the specified URL.
        :param: url: URL to send the request to
        :param data: JSON data to send in the request body
        :return:

        """
        response = requests.put(url, json=data, headers=self.headers)
        response.raise_for_status()
        return response

    def _delete(self, url):
        """
        Send a DELETE request to the specified URL.
        :param: url: URL to send the request to
        :return:

        """
        response = requests.delete(url, headers=self.headers)
        response.raise_for_status()
        return response

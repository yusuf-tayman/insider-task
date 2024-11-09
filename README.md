## Automated API, UI and Performance Testing Tasks

### Project Structure
```
.
├── api_client
│   ├── __init__.py
│   ├── base_client.py
│   ├── pet_client.py
├── base
│   ├── base_test.py
│   ├── page_base.py
│   ├── base_funtions.py
├── pages
│   ├── __init__.py
│   ├── home_page.py
│   ├── careers_page.py
│   ├── jobs_page.py
├── tests
│   ├── api
│   │   ├── test_petstore_api.py
│   ├── ui
│   │   ├── test_careers_page.py
│   ├── load_test
│   │   ├── n11_search.py
├── README.md
├── logger.py
├── conftest.py
├── requirements.txt
```

### Installation
- Clone the repository
- Setup a virtual environment
```bash
pip install virtualenv
virtualenv --python python3 venv
source venv/bin/activate
```

- Install the requirements
```bash
pip install -r requirements.txt
```

### Running the tests
- Run the API tests
```bash
pytest tests/api/test_petstore_api.py
```
- Run the UI tests
```bash
pytest tests/ui/test_careers_page.py --browser=chrome
```
- Run the Load tests
```bash
locust -f tests/load_test/n11_search.py -u 1 -r 1 --headless
```


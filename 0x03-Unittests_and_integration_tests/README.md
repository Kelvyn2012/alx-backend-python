# alx-backend-python

> ALX project repository focused on backend testing (unit & integration) and Python utilities

---

## 📌 Table of Contents

- [About](#about)  
- [Project Structure](#project-structure)  
- [Requirements](#requirements)  
- [Installation](#installation)  
- [Usage](#usage)  
- [Testing](#testing)  
- [Contributing](#contributing)  
- [License](#license)

---

## About

This repository contains exercises and utilities for learning **backend Python development**, with emphasis on:

- Writing **unit and integration tests**  
- Using **mock objects and patches**  
- Parameterizing tests with `parameterized`  
- Building reusable Python utilities (e.g. nested map access, JSON fetching, memoization)  

The goal is to practice writing **robust, well-tested backend code**.

---

## Project Structure

alx-backend-python/
├── 0x01-... # early backend-related projects
├── 0x02-... # context managers / async work
├── 0x03-Unittests_and_integration_tests/
│ ├── utils.py # utility functions
│ ├── client.py # GithubOrgClient class using utils
│ ├── test_utils.py # tests for utils module
│ └── test_client.py # tests for client module
├── README.md
└── other project dirs...


---

## Requirements

- Python **3.7** (Ubuntu 18.04 LTS)  
- `requests` package  
- `parameterized` package (for parameterized tests)  

---

## Installation

1. Clone the repo:

   ```bash
   git clone https://github.com/Kelvyn2012/alx-backend-python.git
   cd alx-backend-python

(Optional) Create a virtual environment:

python3 -m venv venv
source venv/bin/activate


Install dependencies:

pip install -r requirements.txt


If you don’t have a requirements.txt yet, install manually:

pip install requests parameterized

Usage

You can experiment with the utilities interactively:

from utils import access_nested_map

nested = {'a': {'b': 2}}
print(access_nested_map(nested, ('a', 'b')))  # ➝ 2

Testing

All tests are inside 0x03-Unittests_and_integration_tests/.

Run all tests:

python -m unittest discover -v


Run a specific test file:

python -m unittest 0x03-Unittests_and_integration_tests/test_utils.py
python -m unittest 0x03-Unittests_and_integration_tests/test_client.py


Tests cover:

access_nested_map with valid and invalid paths

get_json with mocked HTTP requests

memoize decorator (caching behavior)

GithubOrgClient methods (org, public_repos, has_license)

Contributing

Contributions are welcome 🚀

Fork the repo

Create a branch (feature/my-feature)

Add your changes + tests

Open a pull request

License

📄 License to be decided. If you’d like to use this code, please reach out.


---

Do you want me to also generate a small **`requirements.txt`** file for you so contributors can install everything in one go?

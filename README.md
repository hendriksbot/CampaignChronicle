# CampaignChronicle

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

This app supports DnD session preparation for GMs and chronicles for players

## Set-up

1. Install python 3.14 or higher

2. Create a virtual environtment
    ```
    python -m venv .venv
    ```
3. Activate the virtual environment
    ```
    .venv\Scripts\activate
    ```
4. Install the required packages
    ```
    pip install -e .[dev]
    ```
5. Intstall pre-commit
    ```
    pre-commit install
    ```

6. Test pre-commit
    ```
    pre-commit run --all-files
    ```

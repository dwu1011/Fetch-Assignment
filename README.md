# Points Management API

This project is a simple Flask-based REST API to manage points allocation and spending for different payers. The API allows users to add points, spend points, and check the current balance of points for each payer.

## Features
- **Add Points:** Add points to a payer with a timestamp.
- **Spend Points:** Spend points, ensuring that the oldest points are spent first, and no payer’s balance goes negative.
- **Check Balance:** Retrieve the current balance of points for all payers.

## Files
- **app.py** This is where the actual API endpoints are coded using Flask.
- **pytest.py** This is where the unit tests for the endpoints are housed

## Installation

### Prerequisites
- Python 3.x

### Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/dwu1011/Fetch-Assignment 
   cd Fetch-Assignment
2. Create a Virtual Environment (optional)
    ```bash
    python3 -m venv env
3. Activate Virtual Environment
    ```bash
    source bin/env/activate
4. Install the necessary packages
    ```bash
    python3 install -r requirements.txt
5. Run the App!
    ```bash
    python3 app.py
### Testing

1. Run the Unit Tests
    ```bash
    python3 -m unittest pytest.py
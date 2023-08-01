# Your Project Name

## Overview
A Flask app to provide a report based on sample data from an imaginary e-shop.

## Installation
1. Clone this repository.
2. Create a virtual environment (optional but recommended).
3. Install the required packages using `pip install -r requirements.txt`.

## Usage
1. Run the app using `python run.py`.
2. Access the API endpoint at `http://localhost:5000/api/report?date=YYYY-MM-DD`.
   Replace `YYYY-MM-DD` with the desired date for the report.

## Testing
To run the tests, use the following command:

`python -m unittest discover -s tests -p "tests/test_views.py"`

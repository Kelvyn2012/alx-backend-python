# Python Generators - Data Streaming Project

## Overview

This project explores advanced use of Python generators to efficiently work with large datasets in a MySQL database. It focuses on streaming data row-by-row, batch processing, lazy loading with pagination, and memory-efficient aggregation.

The initial part involves setting up a MySQL database (`ALX_prodev`), creating a `user_data` table, and populating it from a CSV file using a Python script (`seed.py`).

## Project Structure

- `seed.py`: Sets up the MySQL database and table, and loads data from `user_data.csv`.
- `user_data.csv`: Sample CSV file containing user data.
- Other scripts (not shown here) implement generator-based data processing and streaming.

## Requirements

- Python 3.x
- `mysql-connector-python` package (`pip install mysql-connector-python`)
- MySQL server running locally with credentials set in `seed.py`

## Database Schema

**Database:** ALX_prodev  
**Table:** user_data

| Column  | Type         | Constraints                |
| ------- | ------------ | -------------------------- |
| user_id | VARCHAR(36)  | Primary Key, Indexed, UUID |
| name    | VARCHAR(255) | NOT NULL                   |
| email   | VARCHAR(255) | NOT NULL                   |
| age     | DECIMAL      | NOT NULL                   |

## Usage

1. Make sure MySQL server is running and accessible.
2. Adjust MySQL user and password in `seed.py` if needed.
3. Run the setup script:

```bash
python3 0-main.py
```

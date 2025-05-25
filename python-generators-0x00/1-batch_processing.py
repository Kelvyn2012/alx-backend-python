#!/usr/bin/python3
import mysql.connector
from seed import connect_to_prodev  # assuming you have this in seed.py

def stream_users_in_batches(batch_size):
    connection = connect_to_prodev()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM user_data")
    
    batch = []
    for row in cursor:  # Loop 1: iterate over all rows from DB
        batch.append(row)
        if len(batch) == batch_size:
            yield batch
            batch = []
    if batch:  # yield any remaining rows
        yield batch
    
    cursor.close()
    connection.close()

def batch_processing(batch_size):
    for batch in stream_users_in_batches(batch_size):  # Loop 2: get batches
        for user in batch:  # Loop 3: iterate over users in the batch
            if user['age'] > 25:
                print(user)

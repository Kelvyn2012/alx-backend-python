import mysql.connector
import csv

def connect_db():
    """Connect to MySQL server (no database)."""
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",      # change if your user differs
            password=""       # put your MySQL root password here
        )
        return connection
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None

def create_database(connection):
    """Create ALX_prodev database if it doesn't exist."""
    cursor = connection.cursor()
    cursor.execute("CREATE DATABASE IF NOT EXISTS ALX_prodev")
    cursor.close()

def connect_to_prodev():
    """Connect to ALX_prodev database."""
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",    # change if your user differs
            password="",    # your password
            database="ALX_prodev"
        )
        return connection
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None

def create_table(connection):
    """Create user_data table if not exists."""
    cursor = connection.cursor()
    create_table_query = """
    CREATE TABLE IF NOT EXISTS user_data (
        user_id VARCHAR(36) PRIMARY KEY,
        name VARCHAR(255) NOT NULL,
        email VARCHAR(255) NOT NULL,
        age DECIMAL NOT NULL,
        INDEX (user_id)
    )
    """
    cursor.execute(create_table_query)
    connection.commit()
    cursor.close()
    print("Table user_data created successfully")

def insert_data(connection, data_file):
    """Insert data from CSV into user_data table if not exists."""
    cursor = connection.cursor()

    # Read CSV
    with open(data_file, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            # Check if user_id already exists to avoid duplicates
            cursor.execute("SELECT user_id FROM user_data WHERE user_id = %s", (row['user_id'],))
            exists = cursor.fetchone()
            if not exists:
                cursor.execute(
                    "INSERT INTO user_data (user_id, name, email, age) VALUES (%s, %s, %s, %s)",
                    (row['user_id'], row['name'], row['email'], row['age'])
                )
    connection.commit()
    cursor.close()

if __name__ == "__main__":
    conn = connect_db()
    if conn:
        create_database(conn)
        conn.close()
        print("connection successful")

        conn = connect_to_prodev()
        if conn:
            create_table(conn)
            insert_data(conn, 'user_data.csv')

            # Simple test prints
            cursor = conn.cursor()
            cursor.execute("SELECT SCHEMA_NAME FROM INFORMATION_SCHEMA.SCHEMATA WHERE SCHEMA_NAME = 'ALX_prodev'")
            if cursor.fetchone():
                print("Database ALX_prodev is present")
            cursor.execute("SELECT * FROM user_data LIMIT 5")
            print(cursor.fetchall())
            cursor.close()
            conn.close()

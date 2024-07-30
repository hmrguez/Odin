import pandas as pd
import json

import pyodbc
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Retrieve the environment variables
server = os.getenv('DB_SERVER')
database = os.getenv('DB_DATABASE')
username = os.getenv('DB_USERNAME')
password = os.getenv('DB_PASSWORD')

driver_path = '/opt/homebrew/lib/libmsodbcsql.18.dylib'

connection_string = (
    f"Driver={{{driver_path}}};"
    "Server=tcp:odin-ecommerce.database.windows.net,1433;"
    "Database=odin-ecommerce;"
    "Persist Security Info=False;"
    f"Uid={username};"
    f"Pwd={password};"
    "Encrypt=yes;"
    "TrustServerCertificate=no;"
    "Connection Timeout=30;"
)

conn = pyodbc.connect(connection_string)
cursor = conn.cursor()


def load_data_to_db(json_file, table_name):
    # Load JSON data into a DataFrame
    with open(json_file, 'r') as file:
        data = json.load(file)
    df = pd.DataFrame(data)

    if table_name == "Orders":
        df = df.drop(columns=['total_amount'])

    # Insert DataFrame into the SQL table
    for index, row in df.iterrows():

        if table_name == "Products" and (row['product_id'] is None or row['price']) is None:
            continue

        if table_name == "Customers" and row['customer_id'] is None:
            continue

        if (table_name == "Orders" and (row['order_id'] is None
                                        or row['customer_id'] is None or row['product_id'] is None)):
            continue

        try:
            columns = ", ".join(row.index)
            values = ", ".join([f'\'{str(value)}\'' for value in row.values])
            sql_query = f"INSERT INTO {table_name} ({columns}) VALUES ({values})"

            print(sql_query)
            cursor.execute(sql_query)
            conn.commit()
        except Exception as e:
            print(f"Error: {e}")
            continue


if __name__ == "__main__":
    # Load each JSON file
    # load_data_to_db('products.json', 'Products')
    load_data_to_db('customers.json', 'Customers')
    load_data_to_db('orders.json', 'Orders')

    cursor.close()
    conn.close()

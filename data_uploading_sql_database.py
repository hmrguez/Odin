import psycopg2
import pandas as pd
import json

conn = psycopg2.connect(
    host="odin-ecommerce.database.windows.net",
    database="odin-ecommerce",
    user="hmrguez@odin-ecommerce",
    password="111111111",
    port="1433",
)
cursor = conn.cursor()


# Function to load data from JSON to PostgreSQL
def load_data_to_postgres(json_file, table_name):
    with open(json_file, 'r') as file:
        data = json.load(file)
        df = pd.DataFrame(data)

        # Insert data into table
        for index, row in df.iterrows():
            insert_query = f"""
            INSERT INTO {table_name} ({", ".join(df.columns)}) VALUES ({", ".join(['%s'] * len(row))})
            """
            cursor.execute(insert_query, tuple(row))
            conn.commit()


if __name__ == "__main__":
    # Load each JSON file
    load_data_to_postgres('orders.json', 'Orders')
    load_data_to_postgres('products.json', 'Products')
    load_data_to_postgres('customers.json', 'Customers')

    cursor.close()
    conn.close()

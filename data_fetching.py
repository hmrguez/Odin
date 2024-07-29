import requests
import random
import json

# Replace 'your_api_key' with your actual Mockaroo API key
MOCKAROO_API_KEY = '11111111111111111'
MOCKAROO_URL = 'https://api.mockaroo.com/api/generate.json'


# Function to fetch data from Mockaroo
def fetch_mockaroo_data(schema, count):
    response = requests.post(MOCKAROO_URL, json=schema, params={'key': MOCKAROO_API_KEY, 'count': count})
    return response.json()


# Function to introduce corruption in the data
def corrupt_data(data, corruption_rate=0.1):
    for record in data:
        if random.random() < corruption_rate:
            key_to_corrupt = random.choice(list(record.keys()))
            record[key_to_corrupt] = None  # Setting a field to None to simulate corruption
    return data


# Define the schemas
customers_schema = [
    {"name": "customer_id", "type": "Number"},
    {"name": "customer_name", "type": "Full Name"},
    {"name": "email", "type": "Email Address"},
    {"name": "phone", "type": "Phone"},
    {"name": "address", "type": "Address Line 2"}
]

products_schema = [
    {"name": "product_id", "type": "Number"},
    {"name": "product_name", "type": "Product (Grocery)"},
    {"name": "category", "type": "Custom List", "values": ["Fruit", "Vegetable", "Dairy", "Bakery", "Meat"]},
    {"name": "price", "type": "Number", "min": 1, "max": 1000}
]

orders_schema = [
    {"name": "order_id", "type": "Number"},
    {"name": "customer_id", "type": "Number"},
    {"name": "product_id", "type": "Number"},
    {"name": "quantity", "type": "Number", "min": 1, "max": 10},
    {"name": "order_date", "type": "Datetime"},
    {"name": "total_amount", "type": "Formula", "value": "price * quantity"}
]

# Fetch data
num_records = 60
# customers_data = fetch_mockaroo_data(customers_schema, num_records)
products_data = fetch_mockaroo_data(products_schema, num_records)
# orders_data = fetch_mockaroo_data(orders_schema, num_records)
#
# Introduce corruption in the data
corruption_rate = 0.1
# customers_data = corrupt_data(customers_data, corruption_rate)
products_data = corrupt_data(products_data, corruption_rate)
# orders_data = corrupt_data(orders_data, corruption_rate)

# Save data to JSON files
# with open('customers.json', 'w') as f:
#     json.dump(customers_data, f, indent=4)

with open('products.json', 'w') as f:
    json.dump(products_data, f, indent=4)

# with open('orders.json', 'w') as f:
#     json.dump(orders_data, f, indent=4)

print("Data generated and saved to JSON files.")

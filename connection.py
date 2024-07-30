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

print(connection_string)

# Establish a connection to the Azure SQL Database
conn = pyodbc.connect(connection_string)
cursor = conn.cursor()

# Example query to test the connection
cursor.execute("SELECT @@version;")
row = cursor.fetchone()
print(row)

# Close the connection
cursor.close()
conn.close()
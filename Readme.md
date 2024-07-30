Here's a structured README template for your project:

# Data Engineering Project: Azure SQL to Snowflake ETL Pipeline

## Table of Contents

1. [Project Overview](#project-overview)
2. [Architecture](#architecture)
3. [Prerequisites](#prerequisites)
4. [Setup Instructions](#setup-instructions)
   - [Step 1: Set Up Azure Resources](#step-1-set-up-azure-resources)
   - [Step 2: Deploy ARM Template](#step-2-deploy-arm-template)
   - [Step 3: Configure Azure Data Factory](#step-3-configure-azure-data-factory)
5. [Creating Data Factory Pipelines](#creating-data-factory-pipelines)
6. [Data Modeling](#data-modeling)

## Project Overview

This project demonstrates a data engineering workflow that involves uploading data from JSON files to an Azure SQL Database, performing transformations and filtering using Azure Data Factory, and exporting the processed data to a Snowflake database.

## Architecture

![Architecture Diagram](diagram.png)

The architecture consists of the following components:

1. **Azure SQL Database**: Stores the initial data uploaded from JSON files.
2. **Azure Data Factory**: Performs data transformation and filtering.
3. **Snowflake Database**: Stores the final processed data.

## Prerequisites

Before you begin, ensure you have the following:

- An Azure account with necessary permissions.
- A Snowflake account with necessary permissions.
- Azure CLI installed on your local machine.
- Python installed on your local machine.
- Required Python packages: `psycopg2-binary`, `pandas`, `snowflake-connector-python`.

## Setup Instructions

### Step 1: Set Up Azure Resources

> I can't use my own credentials or names here obviously

1. **Create an Azure Resource Group**
   ```bash
   az group create --name yourResourceGroup --location yourLocation
   ```

2. **Create an Azure SQL Database**
   - Navigate to the Azure portal.
   - Create an Azure SQL Database following the instructions provided in the portal.

### Step 2: Deploy ARM Template


1. **Save the ARM Template**
   - Save the ARM template provided above as `deployment.json`.

2. **Deploy the ARM Template**
   ```bash
   az deployment group create --resource-group yourResourceGroup --template-file azure-deploy.json --parameters \
     sqlServerName=your-sql-server \
     sqlServerAdminLogin=sqladmin \
     sqlServerAdminPassword=yourPassword123 \
     sqlDatabaseName=your-sql-database \
     dataFactoryName=your-data-factory \
     snowflakeAccount=your-snowflake-account \
     snowflakeUser=your-snowflake-user \
     snowflakePassword=yourSnowflakePassword123 \
     snowflakeDatabase=your-snowflake-database \
     snowflakeWarehouse=your-snowflake-warehouse
   ```

### Step 3: Configure Azure Data Factory

1. **Create Linked Services**
   - Create linked services for your Azure SQL Database and Snowflake in Azure Data Factory.

2. **Create Datasets**
   - Create datasets corresponding to your Azure SQL Database tables and Snowflake tables.

## Creating Data Factory Pipelines

### Step 1: Create a Pipeline

1. Go to the Azure Data Factory portal.
2. Click on the "Author" icon and then on "Pipelines".
3. Click on "New pipeline".

### Step 2: Add Activities

1. **Add a Copy Data Activity**
   - Drag a "Copy Data" activity to the pipeline canvas.
   - Configure the source to be your Azure SQL Database dataset.
   - Configure the sink to be your Snowflake dataset.

2. **Add Data Flow Activities**
   - Use data flow activities to perform the necessary transformations and filtering (which I described [below](#data-modeling)).
   - Configure the transformations as per your data modeling requirements.

### Step 3: Schedule and Monitor the Pipeline

1. **Add a Trigger**
   - Add a trigger to schedule the pipeline execution at desired intervals.

2. **Monitor the Pipeline**
   - Use the monitoring tools in Azure Data Factory to track pipeline execution and debug any issues.

## Data Modeling

Here we are solving a common problem of data in an ecommerce website. The data 3-fold: products, customers and orders. Data is gathered from the Mockoroo API. Data has a fixed schema which means that it can be stored and uploaded to any SQL database, where I chose an Azure SQL Database. The data is then transformed and filtered using Azure Data Factory and exported to a Snowflake database. To create both SQL database (Azure and Snowflake), we use the following `CREATE TABLE` command, specifying its schema:

```sql
-- Create the Customers table
CREATE TABLE Customers (
    customer_id FLOAT PRIMARY KEY,
    customer_name NVARCHAR(255),
    email NVARCHAR(255) NOT NULL,
    phone NVARCHAR(50),
    address NVARCHAR(255)
);

-- Create the Products table
CREATE TABLE Products (
    product_id FLOAT PRIMARY KEY,
    product_name NVARCHAR(255),
    category NVARCHAR(255),
    price FLOAT
);

-- Create the Orders table
CREATE TABLE Orders (
    order_id FLOAT PRIMARY KEY,
    customer_id FLOAT,
    product_id FLOAT,
    quantity FLOAT,
    order_date DATETIMEOFFSET,
    total_amount NVARCHAR(255),
    FOREIGN KEY (customer_id) REFERENCES Customers(customer_id),
    FOREIGN KEY (product_id) REFERENCES Products(product_id)
);
```

Due to this schema, we enforce some quality checks on the data inserted there. Nothing too complicated. Just make sure that any number field is not null and that the FK constraints from the orders are satisfied.

In the Azure Data Factory pipeline, we perform the following transformations:
1. In Products we filter out any product whose name is null, since there's no evident analysis that could be made from those 
2. In Customers we don't really need to transform or filter out anything for the time being, a user with no name could still be useful for plotting for example `How many users bought a certain product?`. But we could filter out any user with no email, since that's a required field, luckily the pipeline doesn't need to do it, because it's already enforced by the DB
3. In Orders we transform the total_amount field. Because of the nature of the data, it may be wrongfully calculated. Its formula is `quantity * price`. For that we perform a join with the Products table to take the price of the product and then calculate it with the quantity of `self`

Generally, data is ready then to be shipped to Snowflake for further analysis, thus ensuring Data Quality for the time being
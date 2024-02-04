# data_processing/processor.py
import psycopg2
import pandas as pd
from sqlalchemy import create_engine

import os


def connect_to_database():
    try:
        conn = psycopg2.connect(
            host="localhost",
            user="postgres",
            password="barabai123",
            database="dataengineer",
            port="5432"
        )
        return conn
    except Exception as e:
        print(f"Error connecting to the database: {str(e)}")
        return None


def preprocess_data(data):
    # Your data preprocessing logic here

    # Convert "Rp.100.000" format to integer
    data['price'] = data['price'].str.replace('[^\d]', '', regex=True)

    # Convert "Rp.100.000" format to integer for 'price_before'
    data['price_before'] = data['price_before'].str.replace('[^\d]', '', regex=True)

    return data

def store_data_in_database(conn, data):
    try:
        cursor = conn.cursor()

        # Create tables if they don't exist
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS productmaster (
                id SERIAL PRIMARY KEY,
                type VARCHAR,
                name VARCHAR,
                detail TEXT
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS product (
                id SERIAL PRIMARY KEY,
                name VARCHAR,
                price VARCHAR,
                originalprice VARCHAR,
                discountpercentage VARCHAR,
                detail TEXT,
                platform VARCHAR,
                productmasterid INTEGER REFERENCES productmaster(id),
                createdat TIMESTAMP
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS pricerecommendation (
                productid INTEGER REFERENCES product(id),
                price VARCHAR,
                date TIMESTAMP
            )
        """)

        # Commit changes to create tables
        conn.commit()

        # Create a SQLAlchemy engine for PostgreSQL
        engine = create_engine("postgresql://postgres:barabai123@localhost:5432/dataengineer")

        # Insert data into productmaster table
        data_productmaster = data[['category', 'product_name', 'description']].drop_duplicates()
        data_productmaster.columns = ['type', 'name', 'detail']
        data_productmaster.to_sql('productmaster', engine, index=False, if_exists='append')

        # Insert data into product table
        data_product = data[
            ['product_name', 'price', 'price_before', 'discount', 'description', 'platform', 'id', 'datetime']]
        data_product.columns = ['name', 'price', 'originalprice', 'discountpercentage', 'detail', 'platform',
                                'productmasterid', 'createdat']
        data_product.to_sql('product', engine, index=False, if_exists='append')

        # Insert data into pricerecommendation table
        data_pricerecommendation = data[['id', 'price', 'datetime']]
        data_pricerecommendation.columns = ['productid', 'price', 'date']
        data_pricerecommendation.to_sql('pricerecommendation', engine, index=False, if_exists='append')

        cursor.close()
    except Exception as e:
        print(f"Error storing data in the database: {str(e)}")

if __name__ == "__main__":
    # Get the current working directory (where your script is located)
    script_directory = os.path.dirname(os.path.realpath(__file__))

    # Construct the absolute path to the Excel file in the 'crawling' directory
    excel_file_path = os.path.join(script_directory, '..', 'crawling', 'data_product.xlsx')

    # Read the Excel file into a DataFrame
    df = pd.read_excel(excel_file_path)

    # Connect to the PostgreSQL database
    connection = connect_to_database()

    if connection:
        # Preprocess data
        cleaned_data = preprocess_data(df)

        # Store cleaned data in the PostgreSQL database
        store_data_in_database(connection, cleaned_data)

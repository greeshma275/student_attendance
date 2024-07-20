import mysql.connector
import streamlit as st

# Database connection configuration
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'greeshma@123',
    'database': 'college11'  # Replace with your database name
}

# Function to establish database connection
def connect_to_database():
    try:
        connection = mysql.connector.connect(**db_config)
        if connection.is_connected():
            return connection
    except mysql.connector.Error as err:
        st.error(f"Error: {err}")
        return None
connection=connect_to_database()
print(connection)
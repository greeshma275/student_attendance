import streamlit as st
import mysql.connector
from mysql.connector import Error

# Connect to the database
def create_connection():
    connection = None
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="your_username",
            password="your_password",
            database="STUDENT_ATTENDANCE1"
        )
    except Error as e:
        st.error(f"Error: {e}")
    return connection

# Authentication function
def authenticate(username, password, connection):
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM ADMIN WHERE Username=%s AND Password=%s", (username, password))
    result = cursor.fetchone()
    return result is not None

# CRUD operations
def insert_record(query, values, connection):
    cursor = connection.cursor()
    cursor.execute(query, values)
    connection.commit()

def update_record(query, values, connection):
    cursor = connection.cursor()
    cursor.execute(query, values)
    connection.commit()

def delete_record(query, values, connection):
    cursor = connection.cursor()
    cursor.execute(query, values)
    connection.commit()

def fetch_records(query, connection):
    cursor = connection.cursor(dictionary=True)
    cursor.execute(query)
    return cursor.fetchall()

# Streamlit app
st.title("Student Attendance Management System")

# Login Page
st.sidebar.header("Login")
username = st.sidebar.text_input("Username")
password = st.sidebar.text_input("Password", type="password")
if st.sidebar.button("Login"):
    connection = create_connection()
    if authenticate(username, password, connection):
        st.sidebar.success("Logged in successfully!")
        
        # Display and perform CRUD operations
        st.header("Admin Dashboard")
        
        # Create
        if st.button("Insert Sample Data"):
            insert_record(
                "INSERT INTO ADMIN (A_ID, Username, Password) VALUES (%s, %s, %s)",
                (2, 'admin2', 'password2'), connection
            )
            st.success("Sample data inserted.")
        
        # Read
        if st.button("Fetch All Admins"):
            records = fetch_records("SELECT * FROM ADMIN", connection)
            st.write(records)
        
        # Update
        if st.button("Update Sample Data"):
            update_record(
                "UPDATE ADMIN SET Password = %s WHERE A_ID = %s",
                ('newpassword2', 2), connection
            )
            st.success("Sample data updated.")
        
        # Delete
        if st.button("Delete Sample Data"):
            delete_record("DELETE FROM ADMIN WHERE A_ID = %s", (2,), connection)
            st.success("Sample data deleted.")
    else:
        st.sidebar.error("Invalid username or password.")
else:
    st.sidebar.warning("Please log in to access the dashboard.")

import mysql.connector
import streamlit as st

# Database connection configuration
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'greeshma@123',
    'database': 'COLLEGE12'  # Replace with your database name
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
    print(connection)

# Function to execute SQL queries
def execute_query(query, args=None):
    connection = connect_to_database()
    if connection:
        try:
            cursor = connection.cursor()
            if args:
                cursor.execute(query, args)
            else:
                cursor.execute(query)
            connection.commit()
            st.success("Query executed successfully.")
        except mysql.connector.Error as err:
            st.error(f"Error: {err}")
        finally:
            cursor.close()
            connection.close()

# Streamlit UI code for CRUD operations
def main():
    st.title("CRUD Operations with MySQL and Streamlit")

    # Insert operation
    st.header("Insert Operation")
    if st.button("Insert Sample Data"):
        insert_query = "INSERT INTO ADMIN (A_ID, Username, Password) VALUES (1, 'admin1', 'password1')"
        execute_query(insert_query)

    # Update operation
    st.header("Update Operation")
    update_query = "UPDATE ADMIN SET Password = %s WHERE A_ID = %s"
    new_password = st.text_input("New Password")
    a_id_to_update = st.number_input("A_ID to Update", min_value=1, step=1)
    if st.button("Update Password"):
        execute_query(update_query, (new_password, a_id_to_update))

    # Delete operation
    st.header("Delete Operation")
    delete_query = "DELETE FROM ADMIN WHERE A_ID = %s"
    a_id_to_delete = st.number_input("A_ID to Delete", min_value=1, step=1)
    if st.button("Delete Record"):
        execute_query(delete_query, (a_id_to_delete,))

    # Select operation (Read)
    st.header("Select Operation")
    select_query = "SELECT * FROM ADMIN"
    if st.button("Show Admin Records"):
        connection = connect_to_database()
        if connection:
            try:
                cursor = connection.cursor()
                cursor.execute(select_query)
                records = cursor.fetchall()
                if records:
                    st.write("Admin Records:")
                    for record in records:
                        st.write(record)
                else:
                    st.warning("No records found.")
            except mysql.connector.Error as err:
                st.error(f"Error: {err}")
            finally:
                cursor.close()
                connection.close()

if __name__ == "__main__":
    main()

import mysql.connector
import streamlit as st
import pandas as pd  # Import pandas for handling DataFrames

# Database connection configuration
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'greeshma@123',
    'database': 'STUDENT_ATTENDANCE_RECORD'
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

# Function to fetch data
def fetch_query(query):
    connection = connect_to_database()
    if connection:
        try:
            cursor = connection.cursor()
            cursor.execute(query)
            columns = [desc[0] for desc in cursor.description]  # Fetch column names
            result = cursor.fetchall()
            return columns, result
        except mysql.connector.Error as err:
            st.error(f"Error: {err}")
        finally:
            cursor.close()
            connection.close()
    return [], []

# Streamlit UI code for CRUD operations
def main():
    st.title("STUDENT ATTENDANCE RECORD")

    menu = ["Insert", "Read", "Update", "Delete"]
    choice = st.sidebar.selectbox("Menu", menu)

    if choice == "Insert":
        st.subheader("Insert Data")

        table = st.selectbox("Choose Table", ["ADMIN", "BRANCH", "STAFF", "STUDENT", "ATTENDANCE", "ABSENT"])

        if table == "ADMIN":
            a_id = st.number_input("A_ID", min_value=1, step=1)
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            if st.button("Insert"):
                query = "INSERT INTO ADMIN (A_ID, Username, Password) VALUES (%s, %s, %s)"
                execute_query(query, (a_id, username, password))

        elif table == "BRANCH":
            b_id = st.number_input("B_ID", min_value=1, step=1)
            b_name = st.text_input("B_name")
            seat = st.number_input("Seat", min_value=1, step=1)
            a_id = st.number_input("A_ID", min_value=1, step=1)
            if st.button("Insert"):
                query = "INSERT INTO BRANCH (B_ID, B_name, seat, A_ID) VALUES (%s, %s, %s, %s)"
                execute_query(query, (b_id, b_name, seat, a_id))

        elif table == "STAFF":
            staff_id = st.number_input("Staff_ID", min_value=1, step=1)
            name = st.text_input("Name")
            address = st.text_input("Address")
            branch = st.text_input("Branch")
            if st.button("Insert"):
                query = "INSERT INTO STAFF (Staff_ID, Name, Address, Branch) VALUES (%s, %s, %s, %s)"
                execute_query(query, (staff_id, name, address, branch))

        elif table == "STUDENT":
            enroll_no = st.number_input("Enroll_NO", min_value=1, step=1)
            name = st.text_input("Name")
            address = st.text_input("Address")
            branch = st.text_input("Branch")
            b_id = st.number_input("B_ID", min_value=1, step=1)
            if st.button("Insert"):
                query = "INSERT INTO STUDENT (Enroll_NO, Name, Address, Branch, B_ID) VALUES (%s, %s, %s, %s, %s)"
                execute_query(query, (enroll_no, name, address, branch, b_id))

        elif table == "ATTENDANCE":
            attendance_id = st.number_input("Attendance_ID", min_value=1, step=1)
            enroll_no = st.number_input("Enroll_NO", min_value=1, step=1)
            staff_id = st.number_input("Staff_ID", min_value=1, step=1)
            if st.button("Insert"):
                query = "INSERT INTO ATTENDANCE (Attendance_ID, Enroll_NO, Staff_ID) VALUES (%s, %s, %s)"
                execute_query(query, (attendance_id, enroll_no, staff_id))

        elif table == "ABSENT":
            l_id = st.number_input("L_ID", min_value=1, step=1)
            enroll_no = st.number_input("Enroll_NO", min_value=1, step=1)
            reason = st.text_input("Reason")
            days = st.number_input("Days", min_value=1, step=1)
            if st.button("Insert"):
                query = "INSERT INTO ABSENT (L_ID, Enroll_NO, reason, days) VALUES (%s, %s, %s, %s)"
                execute_query(query, (l_id, enroll_no, reason, days))

    elif choice == "Read":
        st.subheader("Read Data")

        table = st.selectbox("Choose Table", ["ADMIN", "BRANCH", "STAFF", "STUDENT", "ATTENDANCE", "ABSENT"])

        if st.button("Fetch Data"):
            query = f"SELECT * FROM {table}"
            columns, results = fetch_query(query)
            if results:
                df = pd.DataFrame(results, columns=columns)
                st.dataframe(df)
            else:
                st.info("No data found.")

    elif choice == "Update":
        st.subheader("Update Data")

        table = st.selectbox("Choose Table", ["ADMIN", "BRANCH", "STAFF", "STUDENT", "ATTENDANCE", "ABSENT"])

        if table == "ADMIN":
            a_id = st.number_input("A_ID", min_value=1, step=1)
            new_password = st.text_input("New Password", type="password")
            if st.button("Update"):
                query = "UPDATE ADMIN SET Password = %s WHERE A_ID = %s"
                execute_query(query, (new_password, a_id))

        elif table == "BRANCH":
            b_id = st.number_input("B_ID", min_value=1, step=1)
            new_seat = st.number_input("New Seat", min_value=1, step=1)
            if st.button("Update"):
                query = "UPDATE BRANCH SET seat = %s WHERE B_ID = %s"
                execute_query(query, (new_seat, b_id))

        elif table == "STAFF":
            staff_id = st.number_input("Staff_ID", min_value=1, step=1)
            new_address = st.text_input("New Address")
            if st.button("Update"):
                query = "UPDATE STAFF SET Address = %s WHERE Staff_ID = %s"
                execute_query(query, (new_address, staff_id))

        elif table == "STUDENT":
            enroll_no = st.number_input("Enroll_NO", min_value=1, step=1)
            new_address = st.text_input("New Address")
            if st.button("Update"):
                query = "UPDATE STUDENT SET Address = %s WHERE Enroll_NO = %s"
                execute_query(query, (new_address, enroll_no))

        elif table == "ABSENT":
            l_id = st.number_input("L_ID", min_value=1, step=1)
            new_days = st.number_input("New Days", min_value=1, step=1)
            if st.button("Update"):
                query = "UPDATE ABSENT SET days = %s WHERE L_ID = %s"
                execute_query(query, (new_days, l_id))

    elif choice == "Delete":
        st.subheader("Delete Data")

        table = st.selectbox("Choose Table", ["ADMIN", "BRANCH", "STAFF", "STUDENT", "ATTENDANCE", "ABSENT"])

        if table == "ADMIN":
            a_id = st.number_input("A_ID", min_value=1, step=1)
            if st.button("Delete"):
                query = "DELETE FROM ADMIN WHERE A_ID = %s"
                execute_query(query, (a_id,))

        elif table == "BRANCH":
            b_id = st.number_input("B_ID", min_value=1, step=1)
            if st.button("Delete"):
                query = "DELETE FROM BRANCH WHERE B_ID = %s"
                execute_query(query, (b_id,))

        elif table == "STAFF":
            staff_id = st.number_input("Staff_ID", min_value=1, step=1)
            if st.button("Delete"):
                query = "DELETE FROM STAFF WHERE Staff_ID = %s"
                execute_query(query, (staff_id,))

        elif table == "STUDENT":
            enroll_no = st.number_input("Enroll_NO", min_value=1, step=1)
            if st.button("Delete"):
                query = "DELETE FROM STUDENT WHERE Enroll_NO = %s"
                execute_query(query, (enroll_no,))

        elif table == "ATTENDANCE":
            attendance_id = st.number_input("Attendance_ID", min_value=1, step=1)
            if st.button("Delete"):
                query = "DELETE FROM ATTENDANCE WHERE Attendance_ID = %s"
                execute_query(query, (attendance_id,))

        elif table == "ABSENT":
            l_id = st.number_input("L_ID", min_value=1, step=1)
            if st.button("Delete"):
                query = "DELETE FROM ABSENT WHERE L_ID = %s"
                execute_query(query, (l_id,))

if __name__ == "__main__":
    main()


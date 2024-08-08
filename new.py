import mysql.connector
import streamlit as st
import pandas as pd

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
    print(f"EXECUTE QUERY FUNCTION: QUERY --> {query}")
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

# Login function with session state
def login():
    session_state = st.session_state
    if 'logged_in' not in session_state:
        session_state.logged_in = False

    st.title("Login")

    correct_username = "admin"
    correct_password = "password"

    # Custom CSS for styling
    st.markdown(
        """
        <style>
        body {
            background-color:#D4B2E0 ;
            font-family: Arial, sans-serif;
        }
        .login-container {
            background-color: #ffffff;
            max-width: 400px;
            padding: 2rem;
            border-radius: 10px;
            box-shadow: 0 0 10px rgba(0,0,0,0.1);
            margin: auto;
            margin-top: 5rem;
        }
        .login-title {
            font-size: 2.5rem;
            font-weight: bold;
            margin-bottom: 1rem;
            text-align: center;
            color: #5F086F;
        }
        .login-form {
            margin-bottom: 1.5rem;
        }
        .login-button {
            width: 100%;
            padding: 1rem;
            border-radius: 5px;
            background-color: #4CAF50;
            color: white;
            font-size: 1.2rem;
            font-weight: bold;
            cursor: pointer;
            transition: background-color 0.3s ease;
        }
        .login-button:hover {
            background-color: #45a049;
        }
        .sidebar-content {
            background-color: lavender;
            color: #333; /* Text color for sidebar */
            padding: 1rem;
            margin-top: 2rem;
            border-radius: 10px;
            box-shadow: 0 0 10px rgba(0,0,0,0.1);
        }
        .sidebar-title {
            font-size: 1.5rem;
            font-weight: bold;
            margin-bottom: 1rem;
            color: #4CAF50;
        }
        .menu-item {
            padding: 0.5rem 1rem;
            margin-bottom: 0.5rem;
            border-radius: 5px;
            cursor: pointer;
            transition: background-color 0.3s ease;
            color: #fff; /* Text color for menu items */
        }
        .menu-item:hover {
            background-color: #45a049;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    # Display the image
    st.image(r"C:\Users\Greeshma G\Pictures\Saved Pictures\image.jpg", width=700)


    st.markdown("<div class='login-title'>Please Enter your details!</div>", unsafe_allow_html=True)
    
    if not session_state.logged_in:
        # Form inputs
        username = st.text_input("Username", key="login_username_input")
        password = st.text_input("Password", type="password", key="login_password_input")

        # Login button
        if st.button("Login"):
            if username == correct_username and password == correct_password:
                session_state.logged_in = True
                st.success(f"Logged in as: {username}")
            else:
                st.error("Incorrect username or password")

    if session_state.logged_in:
        # Logout button
        if st.button("Logout"):
            session_state.logged_in = False
            st.success("Logged out successfully.")

# Streamlit UI code for CRUD operations
def main():
    login()

    if st.session_state.logged_in:
        st.title("STUDENT ATTENDANCE RECORD")

        st.markdown(
            """
            <style>
            /* CSS styling here */
            body {
                background-color: thistle;
                font-family: Arial, sans-serif;
            }
            </style>
            """,
            unsafe_allow_html=True
        )

        menu = ["Staff", "Student", "Admin", "Branch", "Attendance", "Absent"]
        user_choice = st.sidebar.radio("User Type", menu)

        if user_choice == "Staff":
            staff_menu = ["Insert Staff", "Read Staff", "Update Staff", "Delete Staff"]
            staff_choice = st.sidebar.selectbox("Staff Menu", staff_menu)

            if staff_choice == "Insert Staff":
                st.subheader("Insert Staff Data")

                staff_id = st.number_input("Staff ID", min_value=1, step=1)
                name = st.text_input("Name")
                address = st.text_input("Address")
                branch = st.text_input("Branch")
                if st.button("Insert Staff"):
                    query = "INSERT INTO STAFF (Staff_ID, Name, Address, Branch) VALUES (%s, %s, %s, %s)"
                    execute_query(query, (staff_id, name, address, branch))
                    st.success("Staff data inserted successfully.")

            elif staff_choice == "Read Staff":
                st.subheader("Read Staff Data")
                query = "SELECT * FROM STAFF"
                columns, result = fetch_query(query)
                if result:
                    st.write("### Staff Table")
                    df = pd.DataFrame(result, columns=columns)
                    st.write(df)
                else:
                    st.warning("No data found in Staff table.")

            elif staff_choice == "Update Staff":
                st.subheader("Update Staff Data")

                staff_id = st.number_input("Staff ID to Update", min_value=1, step=1)
                name = st.text_input("New Name")
                address = st.text_input("New Address")
                branch = st.text_input("New Branch")
                if st.button("Update Staff"):
                    query = "UPDATE STAFF SET Name = %s, Address = %s, Branch = %s WHERE Staff_ID = %s"
                    execute_query(query, (name, address, branch, staff_id))
                    st.success(f"Staff with ID {staff_id} updated successfully.")

            elif staff_choice == "Delete Staff":
                st.subheader("Delete Staff Data")

                staff_id = st.number_input("Staff ID to Delete", min_value=1, step=1)
                if st.button("Delete Staff"):
                    query = "DELETE FROM STAFF WHERE Staff_ID = %s"
                    execute_query(query, (staff_id,))
                    st.success(f"Staff with ID {staff_id} deleted successfully.")

        elif user_choice == "Student":
            student_menu = ["Insert Student", "Read Student", "Update Student", "Delete Student"]
            student_choice = st.sidebar.selectbox("Student Menu", student_menu)

            if student_choice == "Insert Student":
                st.subheader("Insert Student Data")

                enroll_no = st.number_input("Enroll No", min_value=1, step=1)
                name = st.text_input("Name")
                address = st.text_input("Address")
                branch = st.text_input("Branch")
                b_id=st.number_input("Branch id:",min_value=1,step=1)
                if st.button("Insert Student"):
                    query = "INSERT INTO STUDENT (Enroll_NO, Name, Address, Branch,b_id) VALUES (%s, %s, %s, %s,%s)"
                    execute_query(query, (enroll_no, name, address, branch,b_id))
                    st.success("Student data inserted successfully.")

            elif student_choice == "Read Student":
                st.subheader("Read Student Data")
                query = "SELECT * FROM STUDENT"
                columns, result = fetch_query(query)
                if result:
                    st.write("### Student Table")
                    df = pd.DataFrame(result, columns=columns)
                    st.write(df)
                else:
                    st.warning("No data found in Student table.")

            elif student_choice == "Update Student":
                st.subheader("Update Student Data")

                enroll_no = st.number_input("Enroll No to Update", min_value=1, step=1)
                name = st.text_input("New Name")
                address = st.text_input("New Address")
                branch = st.text_input("New Branch")
                b_id=st.number_input("Branch id",min_value=1,step=1)
                if st.button("Update Student"):
                    query = "UPDATE STUDENT SET Name = %s, Address = %s, Branch = %s ,b_id =%s WHERE Enroll_NO = %s"
                    execute_query(query, (name, address, branch, b_id,enroll_no))
                    st.success(f"Student with Enroll No {enroll_no} updated successfully.")

            elif student_choice == "Delete Student":
                st.subheader("Delete Student Data")

                enroll_no = st.number_input("Enroll No to Delete", min_value=1, step=1)
                if st.button("Delete Student"):
                    query = "DELETE FROM STUDENT WHERE Enroll_NO = %s"
                    execute_query(query, (enroll_no,))
                    st.success(f"Student with Enroll No {enroll_no} deleted successfully.")

        elif user_choice == "Branch":
            branch_menu = ["Insert Branch", "Read Branch", "Update Branch", "Delete Branch"]
            branch_choice = st.sidebar.selectbox("Branch Menu", branch_menu)

            if branch_choice == "Insert Branch":
                st.subheader("Insert Branch Data")

                b_id = st.number_input("B_ID", min_value=1, step=1)
                seat = st.number_input("Seat", min_value=1, step=1)
                a_id = st.number_input("A_ID", min_value=1, step=1)
                b_name = st.text_input("B_Name")
                if st.button("Insert Branch"):
                    query = "INSERT INTO BRANCH (B_ID, Seat, A_ID, B_Name) VALUES (%s, %s, %s, %s)"
                    execute_query(query, (b_id, seat, a_id, b_name))
                    st.success("Branch data inserted successfully.")

            elif branch_choice == "Read Branch":
                st.subheader("Read Branch Data")
                query = "SELECT * FROM BRANCH"
                columns, result = fetch_query(query)
                if result:
                    st.write("### Branch Table")
                    df = pd.DataFrame(result, columns=columns)
                    st.write(df)
                else:
                    st.warning("No data found in Branch table.")

            elif branch_choice == "Update Branch":
                st.subheader("Update Branch Data")

                b_id = st.number_input("B_ID to Update", min_value=1, step=1)
                seat = st.number_input("New Seat", min_value=1, step=1)
                a_id = st.number_input("New A_ID", min_value=1, step=1)
                b_name = st.text_input("New B_Name")
                if st.button("Update Branch"):
                    query = "UPDATE BRANCH SET Seat = %s, A_ID = %s, B_Name = %s WHERE B_ID = %s"
                    execute_query(query, (seat, a_id, b_name, b_id))
                    st.success(f"Branch with B_ID {b_id} updated successfully.")

            elif branch_choice == "Delete Branch":
                st.subheader("Delete Branch Data")

                b_id = st.number_input("B_ID to Delete", min_value=1, step=1)
                if st.button("Delete Branch"):
                    query = "DELETE FROM BRANCH WHERE B_ID = %s"
                    execute_query(query, (b_id,))
                    st.success(f"Branch with B_ID {b_id} deleted successfully.")

        elif user_choice == "Admin":
            admin_menu = ["Insert Admin", "Read Admin", "Update Admin", "Delete Admin"]
            admin_choice = st.sidebar.selectbox("Admin Menu", admin_menu)

            if admin_choice == "Insert Admin":
                st.subheader("Insert Admin Data")

                a_id = st.number_input("A_ID", min_value=1, step=1)
                username = st.text_input("Username")
                password = st.text_input("Password")
                if st.button("Insert Admin"):
                    query = "INSERT INTO ADMIN (A_ID, username, password) VALUES (%s, %s, %s)"
                    execute_query(query, (a_id, username, password))
                    st.success("Admin data inserted successfully.")

            elif admin_choice == "Read Admin":
                st.subheader("Read Admin Data")
                query = "SELECT * FROM ADMIN"
                columns, result = fetch_query(query)
                if result:
                    st.write("### Admin Table")
                    df = pd.DataFrame(result, columns=columns)
                    st.write(df)
                else:
                    st.warning("No data found in Admin table.")

            elif admin_choice == "Update Admin":
                st.subheader("Update Admin Data")

                a_id = st.number_input("A_ID to Update", min_value=1, step=1)
                username = st.text_input("New userame")
                password = st.text_input("New Password")
                if st.button("Update Admin"):
                    query = "UPDATE ADMIN SET username = %s, Password= %s WHERE A_ID = %s"
                    execute_query(query, (username, password, a_id))
                    st.success(f"Admin with A_ID {a_id} updated successfully.")

            elif admin_choice == "Delete Admin":
                st.subheader("Delete Admin Data")

                a_id = st.number_input("A_ID to Delete", min_value=1, step=1)
                if st.button("Delete Admin"):
                    query = "DELETE FROM ADMIN WHERE A_ID = %s"
                    execute_query(query, (a_id,))
                    st.success(f"Admin with A_ID {a_id} deleted successfully.")

        elif user_choice == "Attendance":
            attendance_menu = ["Insert Attendance", "Read Attendance", "Update Attendance", "Delete Attendance"]
            attendance_choice = st.sidebar.selectbox("Attendance Menu", attendance_menu)

            if attendance_choice == "Insert Attendance":
                st.subheader("Insert Attendance Data")
                staff_id = st.number_input("Staff Id", min_value=1, step=1)
                Attendance_id = st.number_input("Attendance Id", min_value=1, step=1)
                enroll_no = st.number_input("Enroll No", min_value=1, step=1)
                date = st.date_input("Date")
                status = st.selectbox("Status", ["Present", "Absent"])

                if st.button("Insert Attendance"):
        # Convert the date to the correct format (YYYY-MM-DD)
                    date_str = date.strftime('%Y-%m-%d')

                    query = "INSERT INTO ATTENDANCE (staff_id,Attendance_id,Enroll_no, Date, Status) VALUES (%s,%s, %s, %s, %s)"
                    execute_query(query, (staff_id, Attendance_id,enroll_no, date, status))

                    st.success("Attendance data inserted successfully.")

            elif attendance_choice == "Read Attendance":
                st.subheader("Read Attendance Data")
                query = "SELECT * FROM ATTENDANCE"
                columns, result = fetch_query(query)
                if result:
                    st.write("### Attendance Table")
                    df = pd.DataFrame(result, columns=columns)
                    st.write(df)
                else:
                    st.warning("No data found in Attendance table.")

            elif attendance_choice == "Update Attendance":
                st.subheader("Update Attendance Data")
                Attendance_id=st.number_input("Attendace Id to update ",min_value=1,step=1)
                staff_id=st.number_input("Staff id to update",min_value=1,step=1)
                enroll_no = st.number_input("Enroll No to Update", min_value=1, step=1)
                date = st.date_input("New Date")
                status = st.selectbox("New Status", ["Present", "Absent"])
                if st.button("Update Attendance"):
                    query = "UPDATE ATTENDANCE SET staff_id = %s,enroll_no=%s,date=%s, status=%s WHERE Attendance_id = %s"
                    execute_query(query, (staff_id,enroll_no,date,status,Attendance_id))
                    st.success(f"Attendance with Enroll No {Attendance_id} updated successfully.")

            elif attendance_choice == "Delete Attendance":
                st.subheader("Delete Attendance Data")

                Attendance_id = st.number_input("Attendance id to Delete", min_value=1, step=1)
                if st.button("Delete Attendance"):
                    query = "DELETE FROM ATTENDANCE WHERE Attendance_id = %s"
                    execute_query(query,(Attendance_id,))
                    st.success(f"Attendance with Attendance id{Attendance_id} deleted successfully.")

        elif user_choice == "Absent":
            absent_menu = ["Insert Absent", "Read Absent", "Update Absent", "Delete Absent"]
            absent_choice = st.sidebar.selectbox("Absent Menu", absent_menu)

            if absent_choice == "Insert Absent":
                st.subheader("Insert Absent Data")
                Absent_id=st.number_input("Absent id ",min_value=1,step=1)
                enroll_no = st.number_input("Enroll No", min_value=1, step=1)
                days = st.number_input("Days",min_value=1,step=1)
                reason = st.text_input("Reason")
                if st.button("Insert Absent"):
                    query = "INSERT INTO ABSENT (Absent_id,Enroll_NO, Days, Reason) VALUES (%s,%s, %s, %s)"
                    execute_query(query, (Absent_id,enroll_no, days, reason))
                    st.success("Absent data inserted successfully.")

            elif absent_choice == "Read Absent":
                st.subheader("Read Absent Data")
                query = "SELECT * FROM ABSENT"
                columns, result = fetch_query(query)
                if result:
                    st.write("### Absent Table")
                    df = pd.DataFrame(result, columns=columns)
                    st.write(df)
                else:
                    st.warning("No data found in Absent table.")

            elif absent_choice == "Update Absent":
                st.subheader("Update Absent Data")
                Absent_id=st.number_input("NEw absent id:",min_value=1,step=1)
                enroll_no = st.number_input("Enroll No to Update", min_value=1, step=1)
                days = st.number_input("New no of days",min_value=1,step=1)
                reason = st.text_input("New Reason")
                if st.button("Update Absent"):
                    query = "UPDATE ABSENT SET enroll_no = %s,days=%s, Reason = %s WHERE Absent_id = %s"
                    execute_query(query, (enroll_no,days, reason,Absent_id))
                    st.success(f"Absent with Absent id {Absent_id} updated successfully.")

            elif absent_choice == "Delete Absent":
                st.subheader("Delete Absent Data")
                Absent_id=st.number_input(" absent id:",min_value=1,step=1)
                if st.button("Delete Absent"):
                    query = "DELETE FROM ABSENT WHERE Absent_id = %s"
                    execute_query(query, (Absent_id,))
                    st.success(f"Absent with Absent id {Absent_id,} deleted successfully.")

if __name__ == "__main__":
    main()
from flask import Flask, render_template_string, request, redirect, url_for, session
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)
app.secret_key = 'admin@123'  # Change this to a secret key for session management

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
    except Error as err:
        return str(err)
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
            return "Query executed successfully."
        except Error as err:
            return f"Error: {err}"
        finally:
            cursor.close()
            connection.close()
    return "Error: Unable to connect to the database."

# Function to fetch data
def fetch_query(query, args=None):
    connection = connect_to_database()
    if connection:
        try:
            cursor = connection.cursor(dictionary=True)
            if args:
                cursor.execute(query, args)
            else:
                cursor.execute(query)
            result = cursor.fetchall()
            return result
        except Error as err:
            return f"Error: {err}"
        finally:
            cursor.close()
            connection.close()
    return []

@app.route('/')
def index():
    if 'logged_in' in session and session['logged_in']:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        query = "SELECT * FROM ADMIN WHERE Username = %s AND Password = %s"
        result = fetch_query(query, (username, password))
        if len(result) > 0:
            session['logged_in'] = True
            return redirect(url_for('dashboard'))
        else:
            return "Invalid username or password."
    return render_template_string('''
        <!DOCTYPE html>
        <html>
        <head><title>Login</title></head>
        <body>
            <h2>Login</h2>
            <form method="post">
                Username: <input type="text" name="username" required><br>
                Password: <input type="password" name="password" required><br>
                <input type="submit" value="Login">
            </form>
        </body>
        </html>
    ''')

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('login'))

@app.route('/dashboard')
def dashboard():
    if 'logged_in' not in session or not session['logged_in']:
        return redirect(url_for('login'))
    return render_template_string('''
        <!DOCTYPE html>
        <html>
        <head><title>Dashboard</title></head>
        <body>
            <h2>Welcome to the Dashboard</h2>
            <a href="{{ url_for('insert') }}">Insert Data</a><br>
            <a href="{{ url_for('read') }}">Read Data</a><br>
            <a href="{{ url_for('update') }}">Update Data</a><br>
            <a href="{{ url_for('delete') }}">Delete Data</a><br>
            <a href="{{ url_for('logout') }}">Logout</a>
        </body>
        </html>
    ''')

@app.route('/insert', methods=['GET', 'POST'])
def insert():
    if request.method == 'POST':
        table = request.form['table']
        if table == 'ADMIN':
            a_id = request.form['a_id']
            username = request.form['username']
            password = request.form['password']
            query = "INSERT INTO ADMIN (A_ID, Username, Password) VALUES (%s, %s, %s)"
            execute_query(query, (a_id, username, password))
        # Handle other tables similarly...
        return redirect(url_for('dashboard'))
    return render_template_string('''
        <!DOCTYPE html>
        <html>
        <head><title>Insert Data</title></head>
        <body>
            <h2>Insert Data</h2>
            <form method="post">
                Table: 
                <select name="table" onchange="changeTable(this.value)">
                    <option value="ADMIN">ADMIN</option>
                    <option value="BRANCH">BRANCH</option>
                    <option value="STAFF">STAFF</option>
                    <option value="STUDENT">STUDENT</option>
                    <option value="ATTENDANCE">ATTENDANCE</option>
                    <option value="ABSENT">ABSENT</option>
                </select><br>
                <div id="form-fields">
                    <!-- Form fields will be added here based on the selected table -->
                </div>
                <input type="submit" value="Insert">
            </form>
            <script>
                function changeTable(table) {
                    let fields = {
                        "ADMIN": `
                            A_ID: <input type="number" name="a_id" min="1" required><br>
                            Username: <input type="text" name="username" required><br>
                            Password: <input type="password" name="password" required><br>
                        `,
                        "BRANCH": `
                            B_ID: <input type="number" name="b_id" min="1" required><br>
                            B_name: <input type="text" name="b_name" required><br>
                            Seat: <input type="number" name="seat" min="1" required><br>
                            A_ID: <input type="number" name="a_id" min="1" required><br>
                        `,
                        "STAFF": `
                            Staff_ID: <input type="number" name="staff_id" min="1" required><br>
                            Name: <input type="text" name="name" required><br>
                            Address: <input type="text" name="address" required><br>
                            Branch: <input type="text" name="branch" required><br>
                        `,
                        "STUDENT": `
                            Enroll_NO: <input type="number" name="enroll_no" min="1" required><br>
                            Name: <input type="text" name="name" required><br>
                            Address: <input type="text" name="address" required><br>
                            Branch: <input type="text" name="branch" required><br>
                            B_ID: <input type="number" name="b_id" min="1" required><br>
                        `,
                        "ATTENDANCE": `
                            Attendance_ID: <input type="number" name="attendance_id" min="1" required><br>
                            Enroll_NO: <input type="number" name="enroll_no" min="1" required><br>
                            Staff_ID: <input type="number" name="staff_id" min="1" required><br>
                        `,
                        "ABSENT": `
                            L_ID: <input type="number" name="l_id" min="1" required><br>
                            Enroll_NO: <input type="number" name="enroll_no" min="1" required><br>
                            Reason: <input type="text" name="reason" required><br>
                            Days: <input type="number" name="days" min="1" required><br>
                        `
                    };
                    document.getElementById('form-fields').innerHTML = fields[table] || '';
                }
            </script>
        </body>
        </html>
    ''')

@app.route('/read', methods=['GET'])
def read():
    table = request.args.get('table')
    query = f"SELECT * FROM {table}"
    results = fetch_query(query)
    return render_template_string('''
        <!DOCTYPE html>
        <html>
        <head><title>Read Data</title></head>
        <body>
            <h2>Read Data from {{ table }}</h2>
            <table border="1">
                <tr>
                    <!-- Add table headers based on table schema -->
                    {% if results|length > 0 %}
                        {% for column in results[0].keys() %}
                            <th>{{ column }}</th>
                        {% endfor %}
                    {% endif %}
                </tr>
                {% for row in results %}
                <tr>
                    {% for value in row.values() %}
                    <td>{{ value }}</td>
                    {% endfor %}
                </tr>
                {% endfor %}
            </table>
            <a href="{{ url_for('dashboard') }}">Back to Dashboard</a>
        </body>
        </html>
    ''', results=fetch_query(f"SELECT * FROM {table}"), table=table)

@app.route('/update', methods=['GET', 'POST'])
def update():
    if request.method == 'POST':
        table = request.form['table']
        if table == 'ADMIN':
            a_id = request.form['a_id']
            new_password = request.form['new_password']
            query = "UPDATE ADMIN SET Password = %s WHERE A_ID = %s"
            execute_query(query, (new_password, a_id))
        # Handle other tables similarly...
        return redirect(url_for('dashboard'))
    return render_template_string('''
        <!DOCTYPE html>
        <html>
        <head><title>Update Data</title></head>
        <body>
            <h2>Update Data</h2>
            <form method="post">
                Table: 
                <select name="table" onchange="changeTable(this.value)">
                    <option value="ADMIN">ADMIN</option>
                    <option value="BRANCH">BRANCH</option>
                    <option value="STAFF">STAFF</option>
                    <option value="STUDENT">STUDENT</option>
                    <option value="ATTENDANCE">ATTENDANCE</option>
                    <option value="ABSENT">ABSENT</option>
                </select><br>
                <div id="form-fields">
                    <!-- Form fields will be added here based on the selected table -->
                </div>
                <input type="submit" value="Update">
            </form>
            <script>
                function changeTable(table) {
                    let fields = {
                        "ADMIN": `
                            A_ID: <input type="number" name="a_id" min="1" required><br>
                            New Password: <input type="password" name="new_password" required><br>
                        `,
                        "BRANCH": `
                            B_ID: <input type="number" name="b_id" min="1" required><br>
                            New Seat: <input type="number" name="new_seat" min="1" required><br>
                        `,
                        "STAFF": `
                            Staff_ID: <input type="number" name="staff_id" min="1" required><br>
                            New Address: <input type="text" name="new_address" required><br>
                        `,
                        "STUDENT": `
                            Enroll_NO: <input type="number" name="enroll_no" min="1" required><br>
                            New Address: <input type="text" name="new_address" required><br>
                        `,
                        "ABSENT": `
                            L_ID: <input type="number" name="l_id" min="1" required><br>
                            New Days: <input type="number" name="new_days" min="1" required><br>
                        `
                    };
                    document.getElementById('form-fields').innerHTML = fields[table] || '';
                }
            </script>
        </body>
        </html>
    ''')

@app.route('/delete', methods=['GET', 'POST'])
def delete():
    if request.method == 'POST':
        table = request.form['table']
        if table == 'ADMIN':
            a_id = request.form['a_id']
            query = "DELETE FROM ADMIN WHERE A_ID = %s"
            execute_query(query, (a_id,))
        # Handle other tables similarly...
        return redirect(url_for('dashboard'))
    return render_template_string('''
        <!DOCTYPE html>
        <html>
        <head><title>Delete Data</title></head>
        <body>
            <h2>Delete Data</h2>
            <form method="post">
                Table: 
                <select name="table" onchange="changeTable(this.value)">
                    <option value="ADMIN">ADMIN</option>
                    <option value="BRANCH">BRANCH</option>
                    <option value="STAFF">STAFF</option>
                    <option value="STUDENT">STUDENT</option>
                    <option value="ATTENDANCE">ATTENDANCE</option>
                    <option value="ABSENT">ABSENT</option>
                </select><br>
                <div id="form-fields">
                    <!-- Form fields will be added here based on the selected table -->
                </div>
                <input type="submit" value="Delete">
            </form>
            <script>
                function changeTable(table) {
                    let fields = {
                        "ADMIN": `
                            A_ID: <input type="number" name="a_id" min="1" required><br>
                        `,
                        "BRANCH": `
                            B_ID: <input type="number" name="b_id" min="1" required><br>
                        `,
                        "STAFF": `
                            Staff_ID: <input type="number" name="staff_id" min="1" required><br>
                        `,
                        "STUDENT": `
                            Enroll_NO: <input type="number" name="enroll_no" min="1" required><br>
                        `,
                        "ATTENDANCE": `
                            Attendance_ID: <input type="number" name="attendance_id" min="1" required><br>
                        `,
                        "ABSENT": `
                            L_ID: <input type="number" name="l_id" min="1" required><br>
                        `
                    };
                    document.getElementById('form-fields').innerHTML = fields[table] || '';
                }
            </script>
        </body>
        </html>
    ''')

if __name__ == '__main__':
    app.run(debug=True)

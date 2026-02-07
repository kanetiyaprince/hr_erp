import pymysql
import os
import ssl  # <--- NEW IMPORT

from flask import Flask, render_template, request

app = Flask(__name__)
app.secret_key = 'prince'

# 1. Database Configuration
db_config = {
    'host': os.environ.get('DB_HOST', 'localhost'),
    'user': os.environ.get('DB_USER', 'root'),
    'password': os.environ.get('DB_PASSWORD', ''),
    'database': os.environ.get('DB_NAME', 'hr_erp_db'),
    'port': int(os.environ.get('DB_PORT', 3306))
}

# 2. Helper function to connect to the database
def get_db_connection():
    # Create a simplified SSL context that accepts "self-signed" certificates
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE

    return pymysql.connect(
        host=db_config['host'],
        user=db_config['user'],
        password=db_config['password'],
        database=db_config['database'],
        port=db_config['port'],
        ssl=ctx # <--- Use the new "relaxed" SSL context
    )

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/contactus")
def contact():
    return render_template("contactus.html")

@app.route("/admin")
def admin():
    return render_template("adminlogin.html")

@app.route("/admindashboard")
def admindashboard():
    return render_template("admin_dashboard.html")

@app.route("/adminaddemp")
def adminaddemp():
    return render_template("admin_addemp.html")

@app.route("/adminshowemp")
def adminshowemp():
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('select emp_id, emp_name, emp_designation from register')
        emplist = cur.fetchall()
        cur.close()
        conn.close()
        return render_template("admin_showemp.html", recordlist=emplist)
    except Exception as e:
        return f"Database Error: {e}"

@app.route("/adminsearchemp")
def adminsearchemp():
    return render_template("admin_searchemp.html")

@app.route("/save", methods=['POST'])
def save():
    try:
        i = request.form['eid']
        n = request.form['ename']
        e = request.form['email']
        m = request.form['mob']
        d = request.form['edesig']
        s = request.form['esalary']

        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute(
            'INSERT INTO register(emp_id, emp_name, emp_email, emp_mobile, emp_designation, emp_salary) VALUES (%s, %s, %s, %s, %s, %s)',
            (i, n, e, m, d, s)
        )
        conn.commit()
        cur.close()
        conn.close()
        return "Successfully added employee"
    except Exception as e:
        return f"Error saving data: {e}"

if __name__ == "__main__":
    app.run(debug=True)
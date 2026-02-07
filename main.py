import pymysql
import os
import ssl  # <--- NEW IMPORT

from flask import Flask, redirect, render_template, request, url_for

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
    ca_path = os.path.join(os.path.dirname(__file__), 'ca.pem')

    return pymysql.connect(
        host=db_config['host'],
        user=db_config['user'],
        password=db_config['password'],
        database=db_config['database'],
        port=db_config['port'],
        ssl={'ca': ca_path}
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
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT emp_id, emp_name, emp_designation FROM register")
    emplist = cur.fetchall()
    cur.close()
    conn.close()
    return render_template("admin_showemp.html", recordlist=emplist)

@app.route("/adminsearchemp", methods=["GET", "POST"])
def adminsearchemp():
    emplist = []
    search_query = ""

    if request.method == "POST":
        search_query = request.form.get("emp", "")

        conn = get_db_connection()
        cur = conn.cursor()

        query = "SELECT * FROM register WHERE emp_name LIKE %s"
        cur.execute(query, (f"%{search_query}%",))
        emplist = cur.fetchall()

        cur.close()
        conn.close()

    return render_template("admin_searchemp.html", employees=emplist, search_query=search_query)

@app.route("/admin_update/<string:emp_id>", methods=["GET", "POST"])
def admin_updateemp(emp_id):
    conn = get_db_connection()
    cur = conn.cursor()

    if request.method == "POST":

        if "delete" in request.form:
            cur.execute("DELETE FROM register WHERE emp_id=%s", (emp_id,))
            conn.commit()
            cur.close()
            conn.close()
            return redirect(url_for("adminshowemp"))

        name = request.form["emp_name"]
        email = request.form["emp_email"]
        desig = request.form["emp_designation"]

        cur.execute("""
            UPDATE register
            SET emp_name=%s, emp_email=%s, emp_designation=%s
            WHERE emp_id=%s
        """, (name, email, desig, emp_id))

        conn.commit()
        cur.close()
        conn.close()
        return redirect(url_for("adminshowemp"))

    cur.execute("SELECT * FROM register WHERE emp_id=%s", (emp_id,))
    data = cur.fetchone()
    cur.close()
    conn.close()

    return render_template("admin_update.html", employee=data)

@app.route("/admin_deleteemp/<string:emp_id>", methods=["POST"])
def admin_deleteemp(emp_id):
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("DELETE FROM register WHERE emp_id=%s", (emp_id,))
    conn.commit()

    cur.close()
    conn.close()

    return redirect(url_for("adminshowemp"))

@app.route("/save", methods=["POST"])
def save():
    i = request.form["eid"]
    n = request.form["ename"]
    e = request.form["email"]
    m = request.form["mob"]
    d = request.form["edesig"]
    s = request.form["esalary"]

    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO register
        (emp_id, emp_name, emp_email, emp_mobile, emp_designation, emp_salary)
        VALUES (%s,%s,%s,%s,%s,%s)
    """, (i, n, e, m, d, s))

    conn.commit()
    cur.close()
    conn.close()

    return "Successfully added employee"

# if __name__ == "__main__":
#     app.run(debug=True)
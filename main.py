import pymysql
import os

from flask import Flask, render_template, request
from flask_mysqldb import MySQL

app = Flask("__name__")

app.secret_key='prince'
app.config['MYSQL_HOST']='localhost'
app.config['MYSQL_USER']='root'
app.config['MYSQL_PASSWORD']='root'
app.config['MYSQL_DB']='hr_erp_db'

mysql = MySQL(app)

db_config = {
    'host': 'mysql-12139fd-hr-erp.j.aivencloud.com', # Copy "Host" from Aiven
    'user': 'avnadmin',                                         # Copy "User" from Aiven
    'password': 'AVNS_Bpoemtss83b6e7ezoz8',                      # Copy "Password" from Aiven
    'database': 'defaultdb',                                    # Copy "Database Name" (usually defaultdb)
    'port': 26797,                                              # Copy "Port" (It will NOT be 3306)
    'ssl_ca': '/etc/ssl/certs/ca-certificates.crt'              # Required for Aiven (keeps connection secure)
}

def get_db_connection():
    # 1. Define the base configuration
    connection_args = {
        'host': db_config['host'],
        'user': db_config['user'],
        'password': db_config['password'],
        'database': db_config['database'],
        'port': db_config['port']
    }

    # 2. Check if we are on Vercel (Linux) or Windows
    # Vercel has this file; Windows does not.
    if os.path.exists('/etc/ssl/certs/ca-certificates.crt'):
        connection_args['ssl'] = {'ca': '/etc/ssl/certs/ca-certificates.crt'}
    
    # 3. Connect using the arguments we built
    return pymysql.connect(**connection_args)

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
    cur = mysql.connection.cursor()

    # Query Specification
    cur.execute('select emp_id,emp_name,emp_designation from register')

    emplist=cur.fetchall()

    return render_template("admin_showemp.html",recordlist=emplist)

@app.route("/adminsearchemp")
def adminsearchemp():
    return render_template("admin_searchemp.html")

@app.route("/save",methods=['post'])
def save():
    i = request.form['eid']
    n = request.form['ename']
    e = request.form['email']
    m = request.form['mob']
    d = request.form['edesig']
    s = request.form['esalary']

    #Database Connection established
    cur = mysql.connection.cursor()

    #Query Specification
    cur.execute('insert into register(emp_id,emp_name,emp_email,emp_mobile,emp_designation,emp_salary) values(%s,%s,%s,%s,%s,%s)',(i,n,e,m,d,s))

    #Transaction Save/Commit
    mysql.connection.commit()

    #Connection Closed
    cur.close()

    return "Successfully added employee"

app.run(debug=True)
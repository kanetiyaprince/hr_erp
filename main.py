import pymysql
import os

from flask import Flask, render_template, request

app = Flask("__name__")
app.secret_key='prince'

db_port = os.getenv('DB_PORT', '12345') 

db_config = {
    'host': os.environ.get('DB_HOST', 'localhost'),
    'user': os.environ.get('DB_USER', 'root'),
    'password': os.environ.get('DB_PASSWORD', ''),
    'database': os.environ.get('DB_NAME', 'hr_erp_db'),
    'port': int(os.environ.get('DB_PORT', 3306)),
    'ssl_ca': '/etc/ssl/certs/ca-certificates.crt'
}

def get_db_connection():
    # Check if we are on Vercel (Linux) to use SSL
    ssl_settings = {}
    if os.path.exists(db_config['ssl_ca']):
        ssl_settings = {'ssl': {'ca': db_config['ssl_ca']}}

    return pymysql.connect(
        host=db_config['host'],
        user=db_config['user'],
        password=db_config['password'],
        database=db_config['database'],
        port=db_config['port'],
        **ssl_settings # Unpack SSL settings if they exist
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

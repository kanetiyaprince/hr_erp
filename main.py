
from flask import Flask, render_template, request,redirect ,url_for
from flask_mysqldb import MySQL

app = Flask("__name__")
# app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

app.secret_key='prince'
app.config['MYSQL_HOST']='localhost'
app.config['MYSQL_USER']='root'
app.config['MYSQL_PASSWORD']=''
app.config['MYSQL_DB']='hr_erp_db'
mysql = MySQL(app)

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


@app.route("/adminsearchemp", methods=['GET', 'POST'])
def adminsearchemp():
    emplist = [] 
    search_query = ''

    if request.method == 'POST':
        search_query = request.form.get('emp', '')
        
        cur = mysql.connection.cursor()
        
        query = "SELECT * FROM register WHERE emp_name LIKE %s"
        search_param = f"%{search_query}%" 
        
        cur.execute(query, (search_param, ))
        
        emplist = cur.fetchall()
        cur.close()

    return render_template("admin_searchemp.html", employees=emplist, search_query=search_query)


@app.route("/admin_update/<string:emp_id>", methods=['GET', 'POST'])
def admin_updateemp(emp_id):
    cur = mysql.connection.cursor()

    if request.method == 'POST':

        if 'delete' in request.form:
            cur.execute("DELETE FROM register WHERE emp_id = %s", (emp_id,))
            mysql.connection.commit()
            cur.close()
            return redirect(url_for('adminshowemp'))

        name = request.form['emp_name']
        email = request.form['emp_email']
        desig = request.form['emp_designation']

        cur.execute("""
            UPDATE register
            SET emp_name=%s, emp_email=%s, emp_designation=%s
            WHERE emp_id=%s
        """, (name, email, desig, emp_id))

        mysql.connection.commit()
        cur.close()
        return redirect(url_for('adminshowemp'))
    cur.execute("SELECT * FROM register WHERE emp_id = %s", (emp_id,))
    data = cur.fetchone()
    cur.close()

    return render_template("admin_update.html", employee=data)


@app.route("/admin_deleteemp/<string:emp_id>", methods=['POST'])
def admin_deleteemp(emp_id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM register WHERE emp_id = %s", (emp_id,))
    mysql.connection.commit()
    cur.close()

    return redirect(url_for('adminshowemp'))



@app.route("/save",methods=['post'])
def save():
    i = request.form['eid']
    n = request.form['ename']
    e = request.form['email']
    m = request.form['mob']
    d = request.form['edesig']
    s = request.form['esalary']

    cur = mysql.connection.cursor()

    cur.execute('insert into register(emp_id,emp_name,emp_email,emp_mobile,emp_designation,emp_salary) values(%s,%s,%s,%s,%s,%s)',(i,n,e,m,d,s))

    mysql.connection.commit()

    cur.close()

    return "Successfully added employee"

app.run(debug=True)
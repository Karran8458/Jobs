from flask import Flask, render_template, request, redirect, session, flash
from mysqlconnection import connectToMySQL    # import the function that will return an instance of a connection
app = Flask(__name__)
app.secret_key = 'keep it safe'
first_name = " "
last_name = " "
email = " "
password = " "
ident = 2
jobid = 4
title = " "
description = " "
address = " "
@app.route("/")
def index():
    return render_template("registration.html")

@app.route('/success', methods=['POST'])
def success():
    global first_name
    global ident
    ident = ident + 1
    fname_for_form = request.form['fname']
    repeat = request.form['psw-repeat']
    if len(fname_for_form) < 3:
        flash("Too short!!!!")
        return redirect("/")
    lname_for_form = request.form['lname']
    if len(lname_for_form) < 3:
        flash("Too short!!!!")
        return redirect("/")
    email_for_form = request.form['email']
    password_for_form = request.form['psw']
    if len(password_for_form) < 8:
        flash("Too short!!!!")
        return redirect("/")
    if len(password_for_form) > 20:
        flash("Too long!!!!")
        return redirect("/")
    if not any(char.isdigit() for char in password_for_form): 
        flash('Password should have at least one numeral') 
        return redirect("/")
    if not any(char.isupper() for char in password_for_form): 
        flash('Password should have at least one uppercase letter') 
        return redirect("/")
    if not any(char.islower() for char in password_for_form): 
        flash('Password should have at least one lowercase letter') 
        return redirect("/")
    if repeat != password_for_form:
        flash('Your password is not confirmed')
        return redirect("/")
    mysql = connectToMySQL('Job2')
    query = "INSERT INTO user (id, first_name, last_name, email, password) VALUES (%(id)s, %(fn)s, %(ln)s, %(e)s, %(p)s);"
    data = {
    
        "id": ident,
        "fn": request.form['fname'],
        "ln": request.form['lname'],
        "e": request.form['email'],
        "p": request.form['psw']
        
    }
    new_user_id = mysql.query_db(query, data)
    return render_template("show.html", fname_on_template=fname_for_form, lname_on_template=lname_for_form, email_on_template=email_for_form)

@app.route('/login_successful', methods=['POST'])
def successful_login():
    global email
    global password
    global first_name
    global last_name
    global ident
    # see if the username provided exists in the database
    email_for_form = request.form['email']
    psw_for_form = request.form['psw']
    if len(psw_for_form) < 8:
        flash("Too short!!!!")
        return redirect("/")
    if len(psw_for_form) > 20:
        flash("Too long!!!!")
        return redirect("/")
    if not any(char.isdigit() for char in psw_for_form): 
        flash('Password should have at least one numeral') 
        return redirect("/")
    if not any(char.isupper() for char in psw_for_form): 
        flash('Password should have at least one uppercase letter') 
        return redirect("/")
    if not any(char.islower() for char in psw_for_form): 
        flash('Password should have at least one lowercase letter') 
        return redirect("/")
    email = email_for_form
    if email == "kman@bellsouth.net":
        first_name = "Karran"
        last_name = "Gowda"
        ident = 1
    if email == "jaypeterson@gmail.com":
        first_name = "Jay"
        last_name = "Peterson"
        ident = 2
    password = psw_for_form
    mysql = connectToMySQL("Job2")
    query = "SELECT * FROM user WHERE email = %(e)s;"
    data = {
    
        "e": request.form['email'] 
        
    }
    result = mysql.query_db(query, data)
    if len(result) > 0:
        return render_template('showlogin.html', all_result = result, email_on_template=email_for_form, first_on_template = first_name)
    flash("You could not be logged in")
    return redirect("/login")
    
@app.route('/logout', methods=['POST'])
def logout():
    global email
    global password
    global first_name
    global last_name
    email = " "
    password = " "
    first_name = " "
    last_name = " "
    return render_template("logout.html")

@app.route('/register', methods=['POST'])
def register():
    return render_template("registration.html")

@app.route('/dash', methods=['POST'])
def dash():
    global first_name
    mysql = connectToMySQL("Job2")
    query = "SELECT * FROM jobs WHERE user_id=%(y)s;"
    data = {
    
        "y": ident 
        
    }
    result = mysql.query_db(query, data)
    mysql = connectToMySQL("Job2")
    query = "SELECT * FROM jobs WHERE user_id!=%(y)s;"
    data = {
    
        "y": ident 
        
    }
    friends = mysql.query_db(query, data)
    return render_template("userdashboard.html", all_users = result, all_results = friends, first_on_template = first_name)

@app.route('/jobs', methods=['POST'])
def wall():
    global first_name
    global email
    mysql = connectToMySQL("Job2")
    query = "SELECT * FROM jobs WHERE user_id=%(y)s;"
    data = {
    
        "y": ident 
        
    }
    users = mysql.query_db(query, data)
    mysql = connectToMySQL("Job2")
    query = "SELECT * FROM jobs WHERE user_id!=%(y)s;"
    data = {
    
        "y": ident 
        
    }
    me = mysql.query_db(query, data)
    mysql = connectToMySQL('Job2')
    query = "SELECT * FROM user WHERE email = %(e)s;"
    data = {
    
        "e": email
        
    }
    result = mysql.query_db(query, data)
    return render_template("userdashboard.html", all_users = users, all_results = result, all_me = me, first_on_template = first_name)

@app.route('/new', methods=['POST'])
def new_job():
    global first_name
    global ident
    global jobid
    global email
    jobid = jobid + 1
    title_for_form = request.form['title']
    if len(title_for_form) < 3:
        flash("Too short!!!!")
        return render_template("addjob.html")
    desc_for_form = request.form['desc']
    if len(desc_for_form) < 3:
        flash("Too short!!!!")
        return render_template("addjob.html")
    address_for_form = request.form['address']
    if len(address_for_form) < 3:
        flash("Too short!!!!")
        return render_template("addjob.html")
    mysql = connectToMySQL('Job2')	        # call the function, passing in the name of our db
    query = "INSERT INTO jobs (id, title, description, address, created_at, updated_at, user_id) VALUES (%(id)s, %(t)s, %(d)s, %(a)s, NOW(), NOW(), %(y)s);"
    data = {
    
        "id": jobid,
        "t": request.form['title'],
        "d": request.form['desc'],
        "a": request.form['address'],
        "y": ident
        
    }
    new_user = mysql.query_db(query, data)
    mysql = connectToMySQL('Job2')
    query = "SELECT * FROM user WHERE email = %(e)s;"
    data = {
    
        "e": email
        
    }
    result = mysql.query_db(query, data)
    return render_template("showlogin.html", all_results = result, first_on_template = first_name)

@app.route("/jobs/<ide>/edit")
def edit_job(ide):
    global first_name
    global email
    mysql = connectToMySQL('Job2')
    query = "SELECT * FROM jobs WHERE id = %(id)s;"
    data = {
    
        "id": ide
        
    }
    result = mysql.query_db(query, data)
    mysql = connectToMySQL('Job2')
    query = "SELECT * FROM user WHERE email = %(e)s;"
    data = {
    
        "e": email
        
    }
    friends = mysql.query_db(query, data)
    return render_template("edit.html", one_result=result, all_freaks = friends, first_on_template = first_name)
    
@app.route("/jobs/<ide>", methods=["POST"])
def view_book(ide):
    global first_name
    global email
    first = " "
    mysql = connectToMySQL('Job2')
    query = "SELECT * FROM jobs WHERE id = %(id)s;"
    data = {
    
        "id": ide
        
    }
    result = mysql.query_db(query, data)
    mysql = connectToMySQL('Job2')
    query = "SELECT * FROM user WHERE email = %(e)s;"
    data = {
    
        "e": email
        
    }
    friends = mysql.query_db(query, data)
    return render_template("view.html", all_result=result, all_friends = friends, first_on_template = first_name)

@app.route("/jobs/<ide>/editjob", methods=["POST"])
def edit_user(ide):
    global first_name
    global email
    title_for_form = request.form['title']
    if len(title_for_form) < 3:
        flash("Too short!!!!")
        return redirect('/jobs/'+ide+'/edit')
    desc_for_form = request.form['desc']
    if len(desc_for_form) < 3:
        flash("Too short!!!!")
        return redirect('/jobs/'+ide+'/edit')
    address_for_form = request.form['address']
    if len(address_for_form) < 3:
        flash("Too short!!!!")
        return redirect('/jobs/'+ide+'/edit')
    mysql = connectToMySQL('Job2')
    query = "UPDATE jobs SET title = %(t)s, description = %(d)s, address = %(a)s WHERE id = %(id)s;"
    data = {
        "id": ide,
        "t": request.form['title'],
        "d": request.form['desc'],
        "a": request.form['address']
    }
    new_user = mysql.query_db(query, data)
    mysql = connectToMySQL("Job2")
    query = "SELECT * FROM jobs WHERE user_id=%(y)s;"
    data = {
    
        "y": ident 
        
    }
    result = mysql.query_db(query, data)
    mysql = connectToMySQL("Job2")
    query = "SELECT * FROM jobs WHERE user_id!=%(y)s;"
    data = {
    
        "y": ident 
        
    }
    me = mysql.query_db(query, data)
    mysql = connectToMySQL('Job2')
    query = "SELECT * FROM user WHERE email = %(e)s;"
    data = {
    
        "e": email
        
    }
    friends = mysql.query_db(query, data)
    return render_template("userdashboard.html", all_users = result, all_results = friends, all_me = me, first_on_template = first_name)

@app.route("/jobs/<ide>/destroy", methods=["POST"])
def destroy_user(ide):
    global identification
    global name
    global email
    global first_name
    mysql = connectToMySQL('Job2')
    query = "DELETE FROM jobs WHERE id = %(id)s;"
    data = {
    
        "id": ide
    }
    new_user = mysql.query_db(query, data)
    mysql = connectToMySQL("Job2")
    query = "SELECT * FROM jobs WHERE user_id=%(y)s;"
    data = {
    
        "y": ident 
        
    }
    result = mysql.query_db(query, data)
    mysql = connectToMySQL("Job2")
    query = "SELECT * FROM jobs WHERE user_id!=%(y)s;"
    data = {
    
        "y": ident 
        
    }
    me = mysql.query_db(query, data)
    mysql = connectToMySQL('Job2')
    query = "SELECT * FROM user WHERE email = %(e)s;"
    data = {
    
        "e": email
        
    }
    friends = mysql.query_db(query, data)
    return render_template("userdashboard.html", all_users = result, all_friends = friends, all_me = me, first_on_template = first_name)

@app.route('/home', methods=['POST'])
def home():
    return redirect("/")

@app.route('/jobs/new', methods=['POST'])
def addjob():
    global first_name
    global email
    mysql = connectToMySQL('Job2')
    query = "SELECT * FROM user WHERE email = %(e)s;"
    data = {
    
        "e": email
        
    }
    friends = mysql.query_db(query, data)
    return render_template("addjob.html", all_friends = friends, first_on_template = first_name)

if __name__ == "__main__":
    app.run(debug=True)

from string import punctuation
from flask import Flask, render_template, request, url_for, redirect, session
import requests
import mysql.connector

#-----------------------------------------------Flask----------------------------------------------

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def Main():
     return render_template('main.html')

@app.route('/login', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if ifExist(username):
            if if_Password_is_right(username,password):
                global UserName 
                UserName = username
                return redirect('/add')
            else:
                return render_template('LoginScreen.html')
    return render_template('login.html')
    
@app.route('/add', methods=['GET', 'POST'])
def add():
    return render_template('add.html')

@app.route('/SignUp', methods=['GET', 'POST'])
def SignUp():
    if request.method == 'POST':
        if 'username' in request.form and 'password' in request.form and 'ConfirmPassword' in request.form:
            username = request.form['username']
            password = request.form['password']
            ConfirmPassword = request.form['ConfirmPassword']
            if password == ConfirmPassword:
                add(username,password)
                return render_template('login.html')
            else:
                return render_template('signup.html')
        else:
            return render_template('signup.html')
    else:
            return render_template('signup.html')

#-----------------------------------------------------SQL------------------------------------------------------------------
## regester the username and password to the database
def add(username,password):
    mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Androwmaged3030",
    database="MovieRecommender"
    )
    mycursor = mydb.cursor()
    sql = "INSERT INTO user (Username, Password, Movies) VALUES (%s, %s, %s)"
    val = (username, password," ")
    mycursor.execute(sql, val)
    mydb.commit()
    mycursor.execute("SELECT * FROM user")
    for x in mycursor:
        print(x)
    mycursor.close()
    mydb.close



## Checking if the name is in the data base
def ifExist(username):
    # Connect to the database
    mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Androwmaged3030",
    database="MovieRecommender"
    )

    # Create a cursor object
    mycursor = mydb.cursor()

    # Query the database
    mycursor.execute("SELECT * FROM user WHERE Username = %s", (username,))

    # Fetch all the results of the query
    result = mycursor.fetchall()

    return result


## Checking if the name is in the data base
def if_Password_is_right(username, password):
    # Connect to the database
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Androwmaged3030",
        database="MovieRecommender"
        )
    try:
        with mydb.cursor() as cursor:
            # Execute the SELECT statement to retrieve the stored password for the given username
            sql = "SELECT Password FROM user WHERE Username = %s"
            cursor.execute(sql, (username,))
            result = cursor.fetchone()
            # Compare the stored password to the input password
            if result['Password'] == password:
                print("Password match.")
            else:
                print("Password does not match.")
    finally:
        mydb.close()

        return result
# -------------------------------------------------------------------------------------------------------------------------
if __name__ == '__main__':
    app.run(debug=True)
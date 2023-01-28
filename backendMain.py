from string import punctuation
from flask import Flask, render_template, request, url_for, redirect, session
import requests


#-----------------------------------------------Flask----------------------------------------------

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def WelcomeScreen():
    return render_template('main.html')

@app.route('/login', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
    #    username = request.form['username']
    #    password = request.form['password']
        #if ifExist(username):
        #    if if_Password_is_right(username,password):
        #        global UserName 
        #        UserName = username
        return redirect('add.html')
    else:
        return render_template('LoginScreen.html')
    return render_template('login.html')


# -------------------------------------------------------------------------------------------------------------------------
if __name__ == '__main__':
    app.run(debug=True)
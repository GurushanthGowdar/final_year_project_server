import pandas as pd
from flask import Flask, render_template, request, redirect, url_for
import numpy as np

app = Flask(__name__)
app.secret_key = 'IDS system'


@app.route("/home")
def home():
    return render_template("index.html")


@app.route('/')
@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        email = request.form["email"]
        pwd = request.form["password"]
        r1 = pd.read_excel('user.xlsx')
        for index, row in r1.iterrows():
            if row["email"] == str(email) and row["password"] == str(pwd):

                return redirect(url_for('home'))
        else:
            mesg = 'Invalid Login Try Again'
            return render_template('login.html', msg=mesg)
    return render_template('login.html')


@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['Email']
        password = request.form['Password']
        col_list = ["name", "email", "password"]
        r1 = pd.read_excel('user.xlsx', usecols=col_list)
        new_row = {'name': name, 'email': email, 'password': password}
        r1 = r1.append(new_row, ignore_index=True)
        r1.to_excel('user.xlsx', index=False)
        print("Records created successfully")
        # msg = 'Entered Mail ID Already Existed'
        msg = 'Registration Successfull !! U Can login Here !!!'
        return render_template('login.html', msg=msg)
    return render_template('register.html')


# @app.route('/password', methods=['POST', 'GET'])
# def password():
#     if request.method == 'POST':
#         current_pass = request.form['current']
#         new_pass = request.form['new']
#         verify_pass = request.form['verify']
#         r1 = pd.read_excel('user.xlsx')
#         for index, row in r1.iterrows():
#             if row["password"] == str(current_pass):
#                 if new_pass == verify_pass:
#                     r1.replace(to_replace=current_pass, value=verify_pass, inplace=True)
#                     r1.to_excel("user.xlsx", index=False)
#                     msg1 = 'Password changed successfully'
#                     return render_template('password_change.html', msg1=msg1)
#                 else:
#                     msg2 = 'Re-entered password is not matched'
#                     return render_template('password_change.html', msg2=msg2)
#         else:
#             msg3 = 'Incorrect password'
#             return render_template('password_change.html', msg3=msg3)
#     return render_template('password_change.html')


def read_excel(file):
    df = pd.read_excel(file)
    cols = list(df.columns)
    df1 = np.asarray(df)
    length = len(df1)
    df2 = []
    count = length
    for i in range(length):
        df2.append(df1[count - 1])
        count -= 1

    return cols, df2


@app.route("/all_ip", methods=['GET', 'POST'])
def all_ip():
    data = read_excel('responsive_ip_log.xlsx')
    title = "List of All Clients"
    return render_template("index.html", title=title, cols=data[0], values=data[1])


@app.route("/blocked_ip", methods=['GET', 'POST'])
def blocked_ip():
    data = read_excel('responsive_blocked_ip.xlsx')
    cols = data[0]
    values = data[1]
    title = "List of Blocked Clients"
    return render_template("index.html", title=title, cols=cols, values=values)


if __name__ == "__main__":
    app.run(debug=True)


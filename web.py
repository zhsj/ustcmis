# -*- coding: utf-8 -*-
from ustcmis import USTCMis
from flask import Flask, session, redirect, url_for, escape, request
import os

app = Flask(__name__)
user = {}


@app.route('/')
def index():
    if check_login():
        return '''
            <p>Logged in as %s</p>
            <p><a href="%s">Grade</a></p>
            <p><a href="%s">Logout</a></p>
        ''' % (session['user'], url_for('get_grade'), url_for('logout'))
    return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST' and 'id' in session:
        user_id = session['id']
        user_code = request.form['user_code']
        pwd = request.form['pwd']
        check_code = request.form['check_code']
        user[user_id].login(user_code, pwd, check_code)
        if user[user_id].login_status:
            session['user'] = user_code
        return redirect(url_for('index'))
    user_id = os.urandom(24)
    user[user_id] = USTCMis()
    session['id'] = user_id
    return '''
        <form action="" method="post">
            <p><input type=text name=user_code></p>
            <p><input type=password name=pwd></p>
            <p><input type=text name=check_code>
            <img src="data:image/jpeg;base64,%s"></p>
            <p><input type=submit value=Login></p>
        </form>
    ''' % user[user_id].get_check_code()


@app.route('/logout')
def logout():
    if 'id' in session:
        user_id = session['id']
        user.pop(user_id, None)
    session.clear()
    return redirect(url_for('login'))


def check_login():
    if 'id' in session and 'user' in session:
        if session['id'] in user and user[session['id']].check_login():
            return True
    return False


@app.route('/grade', methods=['GET', 'POST'])
def get_grade():
    if check_login():
        if request.method == 'POST':
            user_id = session['id']
            semester = request.form['semester']
            content = user[user_id].get_grade(semester)
            return content
        return '''
            <form action="" method="post">
                <p><input type=text name=semester></p>
                <p><input type=submit value=Query></p>
            </form>
        '''
    return redirect(url_for('login'))
# set the secret key.  keep this really secret:
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'

if __name__ == '__main__':
    app.run(debug=True)

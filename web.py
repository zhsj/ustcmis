# -*- coding: utf-8 -*-
from ustcmis import USTCMis
from flask import Flask, session, redirect, url_for, request, json, current_app
import random

app = Flask(__name__)
user = {}
url_prefix = ''


@app.route(url_prefix + '/')
def index():
    if check_login():
        return '''
            <p>Logged in as %s</p>
            <p><a href="%s">Grade</a></p>
            <p><a href="%s">Logout</a></p>
        ''' % (session['user'], url_for('api_get_grade'), url_for('logout'))
    return redirect(url_for('login'))


@app.route(url_prefix + '/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST' and 'id' in session:
        user_id = session['id']
        if user_id not in user:
            return redirect(url_for('login'))
        user_code = request.form['user_code']
        pwd = request.form['pwd']
        check_code = request.form['check_code']
        user[user_id].login(user_code, pwd, check_code)
        session['user'] = user_code
        return redirect(url_for('index'))
    if 'id' in session:
        user_id = session['id']
    else:
        user_id = str(int(random.random() * 1e16))
    user[user_id] = USTCMis()
    session['id'] = user_id
    return '''
        <form action="" method="post">
            <p>User ID<input type=text name=user_code></p>
            <p>Password<input type=password name=pwd></p>
            <p>Captcha<input type=text name=check_code>
            <img src="data:image/jpeg;base64,%s"></p>
            <p><input type=submit value=Login></p>
        </form>
    ''' % user[user_id].get_check_code().encode('base64').replace('\n', '')


@app.route(url_prefix + '/logout')
def logout():
    if 'id' in session:
        user_id = session['id']
        user.pop(user_id, None)
    session.clear()
    return redirect(url_for('login'))


def check_login():
    return 'id' in session and 'user' in session and \
        session['id'] in user and user[session['id']].check_login()


@app.route(url_prefix + '/grade', methods=['GET', 'POST'])
def api_get_grade():
    if check_login():
        try:
            semester = request.values['semester']
        except:
            semester = ''
        user_id = session['id']
        return json_return(user[user_id].get_grade(semester))
    return json_return({'error': 'Not Login'})


def json_return(dict_variable):
    return current_app.response_class(json.dumps(dict_variable,
        indent=2, ensure_ascii=False),
        mimetype='application/json')
# set the secret key.  keep this really secret:
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'

if __name__ == '__main__':
    app.run(debug=True)

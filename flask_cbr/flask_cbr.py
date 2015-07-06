import os
import subprocess
from flask import Flask, render_template, request, \
    session, redirect, url_for, abort, current_app
import hashlib

# Hash of the password used for admin features on the web.

# To create it run python config.py --create_password and copy/paste it into the field below:
password_hash = 'ee26b0dd4af7e749aa1a8ee3c10ae9923f618980772e473f8819a5d4940e0db27ac185f8a0e1d5f84f88bc887fd67b143732c304cc5fa9ad8e6f57f50028a8ff'
# Secret key used by flask, to get a new one run python config.py --create_secret
secret_key = '\xcd/\x06\x99\x83\xc6\xa9\xd9B\xc7\xfd\xe1>\x94Z\xd5\x14\xa0\x00@OK9\xfa'

app = Flask(__name__)
app.secret_key = secret_key
password_hash = password_hash


@app.route('/login', methods=['POST'])
def login_user():
    password = hashlib.sha512(str(request.form['password']).lower()).hexdigest()
    if password == password_hash:
        session['logged_in'] = True

    return redirect(url_for('home'))


@app.route('/logout', methods=['POST'])
def logout_user():
    if session.get('logged_in'):
        session.pop('logged_in', None)
        return redirect(url_for('home'))
    return abort(404)


@app.route('/execute', methods=['POST'])
def execute_command():
    if not session.get('logged_in'): return abort(403)
    command = request.form.get('command')
    if not command:
        return "No command specified"
    bankfrom = os.path.join(current_app.root_path, 'cbr-db/py3/bankform.py')
    proc = subprocess.Popen(
        ['/usr/bin/python3 {} {} '.format(bankfrom, command)],
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )

    out, err = proc.communicate()
    resp = out.decode('utf-8')
    resp += err.decode('utf-8')

    return resp


@app.route('/pull', methods=['POST'])
def git_pull():
    if not session.get('logged_in'): return abort(403)
    gitpull = os.path.join(current_app.root_path, 'gitpull.sh')
    proc = subprocess.Popen(
        ['/bin/bash ' + gitpull],
        shell=True,
        stdout=subprocess.PIPE
    )

    resp = proc.communicate()[0].decode('utf-8')
    return resp


@app.route('/')
def home():
    return render_template('base.html')


if __name__ == '__main__':
    app.debug = True
    app.run()

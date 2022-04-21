from flask import Flask, render_template, redirect, request, url_for, session
from pymongo import MongoClient
from bson.objectid import ObjectId
import os

app = Flask(__name__)
app.secret_key = 'some secret'

cluster = MongoClient('mongodb+srv://admin:N4yqaCy7BTzZe8sw@resumegeneratorcluster.0spsy.mongodb.net/resume-generator')
db = cluster['resume-generator']
users = db['users']

@app.route('/')

@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'username' in session:
        return render_template('index.html',
                                message='You are already logged in!')
    if request.method == 'POST':
        users = db['users']
        user_login = users.find_one({'username': request.form['username']})
        if user_login:
            if request.form['password'] == user_login['password']:
                session['username'] = request.form['username']
                return redirect(url_for('index'))
        return render_template('login.html',
                                    message='Invalid username or password')
    return render_template('login.html', message='')

@app.route('/logout')
def logout():
    if 'username' in session:
        session.pop('username')
        return render_template('message.html',
                                message='Logged out. See you later!')
    return render_template('message.html',
                            message='You have already logged out!')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if 'username' in session:
        return render_template('register.html',
                                message='You are already logged in and registered')
    if request.method== 'POST':
        users = db['users']
        existing_user = users.find_one({'username': request.form['username']})
        if request.form['username'] and request.form['password']:
            if existing_user is None:
                password = request.form['password']
                users.insert_one({'username': request.form['username'],
                                'password': password})
                session['username'] = request.form['username']
                return redirect(url_for('index'))
            return render_template('register.html', message='Username ' + str(existing_user['username']) + ' already exists')
        return render_template('register.html', message='Enter a username and password')
    return render_template('register.html', message='')


@app.route('/<username>/add_resume', methods=['GET', 'POST'])
def add_resume(username):
    if 'username' in session:
        username = session['username']
        if request.method == 'POST':
            resume = db['resumes']
            resume.insert_one({
                # Contact Details
                'first_name': request.form['first_name'],
                'last_name': request.form['last_name'],
                'address': session['address'],
                'mobile_number': session['mobile_number'],
                'email_address': session['email_address'],
                # Work History
                'company_name': session['company_name'],
                'position': session['position'],
                'start_date': session['start_date'],
                'end_date': session['end_date'],
                'main_duties': session['main_duties'],
                
            })
        return render_template('addresume.html',
                                username=session['username'])
    return render_template('login.html')

if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
    port=int(os.environ.get('PORT', 5000)),
    debug=True)
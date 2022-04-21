from flask import Flask, render_template, redirect, request, url_for, session
from pymongo import MongoClient
from bson.objectid import ObjectId
import os

app = Flask(__name__)
app.secret_key = 'some secret'


@app.route('/')

@app.route('/index')
def index():
    return render_template('index.html')


if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
    port=int(os.environ.get('PORT', 5000)),
    debug=True)
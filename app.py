#! /usr/bin/env python3
from flask import Flask, jsonify, request, redirect, render_template
from flask_cors import CORS
import flask_sqlalchemy as sqlalchemy
import datetime
#import smtplib #for if you want to send emails
#import os #for other things
#import hashlib #for hashes - prob wont need
#also import backend files here

app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sqlalchemy-demo.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True #im not sure what this does, but there was an error that said to set it to either True or False so...
base_url = '/api/'
db = sqlalchemy.SQLAlchemy(app)

class Comments(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    com = db.Column(db.String)

@app.route("/index.html")
@app.route("/")
def hello():
    return render_template('./index.html') #renember to put html in templates

@app.route(base_url + 'setComments', methods=['POST'])
def setComment():
    dat = 0
    dat = request.get_json()
    myComment = dat['comment']
    print(myComment)
    db.session.add(myComment)
    db.session.commit()

def main():
    app.run()

if __name__ == '__main__':
    main()

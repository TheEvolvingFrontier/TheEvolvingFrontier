#! /usr/bin/env python3
from flask import Flask, jsonify, request, redirect, render_template
import flask_cors import CORS
import flask_sqlalchemy as sqlalchemy
import datetime
#import smtplib #for if you want to send emails
#import os #for other things
#import hashlib #for hashes - prob wont need
#also import backend files here

app = Flask(__name__)
CORS(app)
base_url = '/api/'
db = sqlalchemy.SQLAlchemy(app)

class Comments(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	com = db.Column(db.String)

@app.route("/index.html")
@app.route("/")
def hello():
	return render_template('./yourhtmlfilehere') #renember to put html in templates

@app.route(base_url + 'getComments', methods=['POST'])
	dat = request.get_json()
	myComment = dat['comment']
	print(myComment)
	db.session.add(myComment)
	db.session.commit()

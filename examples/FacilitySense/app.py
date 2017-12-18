#! /usr/bin/env python3
#app.py - the core of the app. This is origionally Tyler's code to help us with the Smile project, but we're using is to help our project too.

from flask import Flask, jsonify, request, redirect, render_template
from flask_cors import CORS
import flask_sqlalchemy as sqlalchemy
import smtplib #for email sending
import datetime
import os #used fore RNG and undoubtly many other things
import hashlib
import accounts #accounts code
import comments

app = Flask(__name__)  #, template_folder='../pages/templates')
CORS(app)
commentsList = comments.loadComments()
accountList = accounts.loadAccounts()
base_url = '/api/'

@app.route('/index.html')
@app.route('/')
def signinpage():
    print('in sign in page, index.html')
    return render_template('./index.html')

#@app.route('/css/style.css')
#@app.route('/style.css')
#def styles():
#    print('in styles')
#    return render_template('./css/style.css')

@app.route('/newAccountVerification.html')
def newaccver():
    print('newAccountVerification')
    return render_template('./newAccountVerification.html')

@app.route('/newAccountEmail.html')
def newAccountEmail():
    print('newAccountEmail')
    return render_template('./newAccountEmail.html')

@app.route('/facilitySense.html')
def fac():
    print('facilitySense')
    return render_template('./facilitySense.html')

#@app.route('/facScripts.js')
#@app.route('/scripts/facScripts.js')
#def facScripts():
#    print('facScripts')
#    return render_template('./scripts/facscripts')

@app.errorhandler(404)
def page_not_found(e):
    return redirect('http://kvartirakrasivo.ru/404/index.php') #this is a sketchy looking URL

@app.route(base_url + 'getComments', methods=['POST'])
def getComments():

    dat = request.get_json()
    x = int(dat['x'])
    y = int(dat['y'])
    number = 4 * y + x + 1
    formatedComments = ''
    try:
        formatedComments = comments.formatCommentsForPrinting(comments.findComments(str(number),commentsList,"",""))
    except:
        formatedcomments = 'comments for ' + str(number)
    print(formatedComments)
    return jsonify({"status":1, "comments":formatedComments },200)
    #comments.findComments(str(x) + ' ' + str(y),
    #print(comments.findComments(str(number),commentList,"",""))
    #print(formatCommentsForPrinting(comments.findComments(str(number),commentList,"","")))

@app.route(base_url + 'postComment', methods=['POST'])
def postCom():
    dat = request.get_json()
    print(dat['comment'])
    commentsList.append(comments.addComment("UsernamePlaceholder",dat['comment'],"a long time ago, actually never, and also now","","",str(int(dat["loc"])+1),"Good"))#should work
    comments.storeComments(commentsList)
    return jsonify({"status":1},200)

@app.route(base_url + 'newaccount', methods=['POST'])
def VerfiyEmail():
    print('in email verification')
    print('--')
    dat = (request.get_json())
    print(dat['email'])
    newuseraccount = accounts.userAccount()
    newuseraccount.email = dat['email']
    print(accountList)
    accounts.sendUserVerificationEmail(newuseraccount) #if this doesnt work then it should throw an error or something and not return 200. Make it return a bool and i will do some if statement stuff
    accountList.append(newuseraccount)
    accounts.storeAccounts(accountList) # we store the list now that we have
    return jsonify({"status":1, "url":"./newAccountVerification.html?email=" + dat['email']},200)


@app.route(base_url + 'accountinfo', methods=['POST'])
def CreateAccount():
    dat = request.get_json()
    usr = dat['usr']
    pswd = dat['pswd']
    code = dat['code']
    email = dat['email']
    myUsr = accounts.getUser(email, accountList)
    if myUsr == None:
        return jsonify({"status":0, "url":"/"}, 500)
    print('old vals - usr: ' + myUsr.userName +', pswd: ' + myUsr.password + ', code: ' + myUsr.verificationCode + ', email: ' + myUsr.email )
    if myUsr.verificationCode != code:
        return jsonify({"status":0, "url":"/newAccountEmail.html"}, 400)
    myUsr.email = email
    myUsr.userName = usr
    myUsr.password = pswd
    myUsr.isVerified = True
    print('new vals - usr: ' + usr +', pswd: ' + pswd + ', code: ' + code + ', email: ' + email)
    print(usr + ',' + pswd + ',' + code)
    accounts.checkForVerification(myUsr,code) #use this to do it. user is the user object. codeProvided is he code th user entered. it it meatches the code in their file, their verified states changes to true ##this should work now
    return jsonify({"status":1, "url":'./facilitySense.html'},200)

def main():
     app.run() # runs the Flask application

if __name__ == '__main__':
    main()


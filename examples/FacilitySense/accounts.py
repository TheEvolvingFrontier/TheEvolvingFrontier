#accounts.py - handles user accounts

import datetime
import os #used for RNG and undoubtly many other things
import hashlib
import smtplib


def genVerificationCode(): # now just a wrapper for genRandomCode
    return genRandomCode()

def genRandomCode():
    randomstring = os.urandom(256)
    hashedrandomstring =  hashlib.sha224(randomstring).hexdigest()
    return hashedrandomstring

class userAccount:
    def __init__(self):
        verificationCode = genRandomCode()
    def setAll(self,FN,LN,UN,EM,PWD,isVER,VC):
        self.firstName = FN
        self.lastName = LN
        self.userName = UN
        self.email = EM
        self.password = PWD
        self.isVerified = isVER
        self.verificationCode = VC
    firstName = ""
    lastName = ""
    userName = ""
    email = ""
    password = "" #fix this in iteratiion 3! ##fix what? ### the fact that we store passwords in plaintext. I know this is a student project, but that's just bad secutiry pratice.
    isVerified = False
    verificationCode = "" #used to verify users. we set this when we send a verification email and check it when the user attempts verification

def getUser( email, accountList ):
    for account in accountList:
        if account.email == email:
           return account
    return None

def sendUserVerificationEmail(user): ##sends the email to verify users
    secureCode = genVerificationCode()
    user.verificationCode = secureCode

    ##code form here: http://naelshiab.com/tutorial-send-email-python/

    #its possible that it wont let you send email. This is because google gets
    #nervous when a ton of people use the same account. So make a new one.
    #put creds below.

    #facilitysensev2@gmail.com - qwertyuiop!1
    #facilitysense.best322@gmail.com - computerscience322
    server = smtplib.SMTP('smtp.gmail.com', 587)
    print('1')
    server.starttls()
    print('2')
    server.login("facilitysensev2@gmail.com", "qwertyuiop!1")
    print('3')
    msg = "Here is your Verification code:\n\n" + secureCode + "\n\nNow Please enter it exactly as it appears to verify your account."
    print("if we got here, we're probably sending the email just fine")
    server.sendmail("facilitysensev2@gmail.com", user.email, msg)
    server.quit()

def checkForVerification(user,codeProvided):
    if(user.verificationCode == codeProvided):
        user.isVerified = True

def loadAccounts():
    accountFile = open('users.csv', 'r')
    accountList = []
    accountFileList = accountFile.readlines()
    accountFile.close()
    for account in accountFileList:
        templist = [x.strip() for x in account.split(',')]
        what = userAccount()
        what.setAll(templist[0], templist[1], templist[2], templist[3], templist[4], bool(templist[5]), templist[6])
        accountList.append(what)
    return accountList

def storeAccounts(accountList):
    accountFile = open('users.csv', 'w')
    for account in accountList:
        accountFile.write(account.firstName + "," + account.lastName + "," + account.userName + "," + account.email + "," + account.password + "," + str(account.isVerified) + "," + account.verificationCode + "\n")
    accountFile.close()

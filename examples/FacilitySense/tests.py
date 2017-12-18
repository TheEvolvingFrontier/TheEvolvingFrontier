#tests.py - automated regression tests for our code

import accounts

import comments

#tests for bugs in the accounts system

#tests for bugs in account handling code

newFirstName = "john"

newLastName = "doe"

newUsername = "jdoe"

newEmail = "chanse.cramer@wsu.edu" #real for testing actual code

newPassword = "123456"

newIsVerified = True

NewVerificationCode = accounts.genVerificationCode()


newaccount = accounts.addAccount(newFirstName, newLastName, newUsername, newEmail, newPassword, newIsVerified, newVerificationCode)

if(newaccount.firstName != newFirstName or newEmail != newaccount.email or newIsVerified != newaccount.isVerified):

    print("something went wrong in the addaccount function")

else: print("everything is fine")




#tests for regression in the verification code system

diffrent1 = accounts.genVerificationCode()

diffrent2 = accounts.genVerificationCode()

if(diffrent1 == diffrent2):
    print("ERROR: genVerificationCode() returning same values")

else: print("genVerificationCode() is working fine")



accounts.sendUserVerificationEmail(newaccount) #should get an email from this, perform manually

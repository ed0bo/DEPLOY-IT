from __future__ import unicode_literals
from django.db import models
import bcrypt
import re

class UserManager(models.Manager):
    def registrationValidator(self, postData):
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        errors = {}

        if len(postData['firstName']) < 2:
            errors['firstName'] = "First Name must be at LEAST 2 characters plz"

        if len(postData['lastName']) < 2:
            errors['lastName'] = "Last Name must be at LEAST 2 characters plz"

        if not EMAIL_REGEX.match(postData['email']):
            errors['email'] = "No special characters in your Email plz"

        try:
            if User.objects.get(email = postData['email']):
                errors['emailDupe'] = "Email is already in use bruh"
        except:
            pass

        if len(postData['userName']) < 2:
            errors['userName'] = "User name must be at LEAST 2 characters plz"

        if (User.objects.filter(userName = postData['userName'])):
            errors['userNameDupe'] = "User name is already in use bruh"

        if len(postData['password']) < 5:
            errors['password'] = "Password must be at LEAST 5 characters plz"

        if postData['password'] != postData['confirmPassword']:
            errors['confirmPassword'] = "Type your passwords correctly plz"
        return errors
        
    def loginValidator (self,postData):
        errors = {}
        user = ""
        try:
            user = User.objects.get(userName = postData['loginUserName'])
        except:
            errors['userNameNotFound'] = "Make sure login info is correct plz"

        try:
            bcrypt.checkpw(postData['loginPassword'].encode('utf-8'), user.password.encode('utf-8'))
        except:
            errors['userNameNotFound'] = "Make sure login info is correct plz"

        return errors
    
    def quoteValidator (self, postData):
        errors = {}
        if len(postData['author']) < 3:
            errors['author'] ="uuhhh, no on your author"
        if len(postData['quote']) < 10:
            errors['quote'] = "hmm..... no on your quote"
        return errors

    def updateValidator (self, postData):
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        errors = {}
        if len(postData['firstName']) < 2:
            errors['firstName'] = "First Name must be at LEAST 2 characters plz"

        if len(postData['lastName']) < 2:
            errors['lastName'] = "Last Name must be at LEAST 2 characters plz"

        if not EMAIL_REGEX.match(postData['email']):
            errors['email'] = "No special characters in your Email plz"

        try:
            if User.objects.get(email = postData['email']):
                errors['emailDupe'] = "Email is already in use bruh"
        except:
            pass

        return errors
        
class User (models.Model):
    firstName = models.CharField(max_length = 255)
    lastName = models.CharField(max_length = 255)
    userName = models.CharField(max_length = 255)
    email = models.CharField(max_length = 255)
    password = models.CharField(max_length = 255)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = UserManager()
    def __repr__(self):
        return"<User object - firstName: {}, lastName: {}, email: {}>".format(self.firstName, self.lastName, self.email)

class Quote (models.Model):
    author = models.CharField(max_length = 255)
    quoteContent = models.TextField()
    postedBy = models.ForeignKey (User, related_name = "quotesPosted")
    likedBy = models.ManyToManyField (User, related_name = "likes")
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = UserManager()
    def __repr__(self):
        return"<Book Quote - author: {}, quoteContent: {}, postedBy: {}, likedBy: {} >".format(self.author, self.quoteContent, self.postedBy, self.likedBy)
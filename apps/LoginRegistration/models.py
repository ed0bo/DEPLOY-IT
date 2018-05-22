from __future__ import unicode_literals
from django.db import models
import bcrypt
import re

class UserManager(models.Manager):
    def registrationValidator(self, postData):
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        errors = {}

        if len(postData['firstName']) < 2:
            errors['firstName'] = "First name must be at LEAST 2 characters plz"

        if len(postData['lastName']) < 2:
            errors['lastName'] = "Last name must be at LEAST 2 characters plz"

        if not EMAIL_REGEX.match(postData['email']):
            errors['email'] = "No special characters in your Email plz"

        try:
            if User.objects.get(email = postData['email']):
                errors['emailDupe'] = "Email is already in use DB bruh"
        except:
            pass
        if len(postData['userName']) < 2:
            errors['userName'] = "User name must be at LEAST 2 characters plz"

        if (User.objects.filter(userName = postData['userName'])):
            errors ['userNameDupe'] = "User name is already in use bruh"

        if len(postData['password']) < 5:
            errors['password'] = "Password must be at LEAST 5 characters plz"

        if postData['password'] != postData['confirmPassword']:
            errors['confirmPassword'] = "Type your passwords correctly plz"
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
        return"<User object - firstName: {}, lastName: {}, email: {}".format(self.firstName, self.lastName, self.email)
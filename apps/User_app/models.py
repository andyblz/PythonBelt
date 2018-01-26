# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.
import re
import bcrypt

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')


class UserManager(models.Manager):
    def add_user(self, data):
        errors = []
        if len(data['name']) < 2:
            errors.append('Name must be at least 2 characters long.')
       
        if not data['email']:
            errors.append('Email field in required')
        if not EMAIL_REGEX.match(data['email']):
            errors.append('Enter a valid email')
        if len(data['password']) < 8:
            errors.append('Password must be at least 8 characters long.')
        if data['password'] != data['cpassword']:
            errors.append('Password must match.')

        user = self.filter(email=data['email'])
        if user:
            errors.append('Email already exists')

        response = {}
        if errors:
            response['status'] = False
            response['errors'] = errors

        else:
            hashed_password = bcrypt.hashpw(data['password'].encode(), bcrypt.gensalt())
            user = self.create(name = data['name'], email = data['email'], password = hashed_password)
            response['status'] = True
            response['user'] = user

        return response

    def validate_user(self, data):
        user = self.filter(email=data['email'])
        errors = []
        response = {}
        if user:
            if bcrypt.hashpw(data['password'].encode(), user[0].password.encode()) == user[0].password.encode():
               
                response['status'] = True
                response['loggedin_user'] = user[0]
            else:
               
                errors.append('Invalid email')
                response['status'] = False
                response['errors'] = errors
        else:
            
            errors.append('Invalid Email')
            response['status'] = False
            response['errors'] = errors

        return response

class User(models.Model):
    name = models.CharField(max_length = 45)  
    email = models.CharField(max_length = 255)
    password = models.CharField(max_length = 255)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = UserManager()

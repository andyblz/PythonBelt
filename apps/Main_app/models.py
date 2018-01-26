# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

from datetime import date
from ..User_app.models import User
# Create your models here.

class Trip_manager(models.Manager):
    def valid_trip(self, data):
        response = {}
        errors = []
        if len(data['name']) < 1:
            errors.append("Name required")
        if len(data['desc']) < 1:
            errors.append("Description required")
        if len(data['td_from']) < 1:
            errors.append("Start Date required")
        if len(data['td_to']) < 1:
            errors.append("End Date required")
        if errors:
            response['status'] = False
            response['errors'] = errors
        else:
            response['status'] = True
           

            self.create(name = data['name'], desc = data['desc'], td_from = data['td_from'], td_to = data['td_to'])

        return response
class Trip(models.Model):
    name = models.CharField(max_length=255)
    desc = models.CharField(max_length=255)
    td_from = models.DateField()
    td_to = models.DateField()
   
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    users = models.ManyToManyField(User, related_name="trips")
    objects = Trip_manager()
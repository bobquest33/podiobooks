"""Profile Module Models File"""

from __future__ import division
from django.db import models
from django.contrib.auth.models import User
import datetime
from django.template.defaultfilters import slugify


class UserProfile(models.Model):
    """Information about the user which we need for preferences, social needs,
    etc."""
    user = models.ForeignKey(User, related_name='userprofile') #User is an OOTB Django Auth Model
    slug = models.SlugField()
    date_created = models.DateTimeField(default=datetime.datetime.now())
    date_updated = models.DateTimeField(default=datetime.datetime.now())
        
    def __unicode__(self):
        return "UserProfile"
    
    def save(self):
        if not self.id:
            self.slug = slugify(self.user.username)

        super(UserProfile, self).save()
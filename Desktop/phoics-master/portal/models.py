from __future__ import unicode_literals

from django.db import models
STATUS_CHOICES = ((1, "Private"),(2, "Public"),)
class Document(models.Model):
    document = models.FileField(upload_to='documents/')
    status = models.IntegerField(choices=STATUS_CHOICES, default=1)
    uploaded_at = models.DateTimeField(auto_now_add=True)

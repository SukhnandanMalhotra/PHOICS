from __future__ import unicode_literals

from django.db import models


choice = (("PRIVATE", "Private"),("PUBLIC", "Public"),)
class Document(models.Model):
    status=models.CharField(max_length=7,choices=choice)
    document = models.FileField(upload_to='documents/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
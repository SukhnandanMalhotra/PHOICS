from __future__ import unicode_literals
from django.utils import timezone
from django.db import models


choice = (("PRIVATE", "Private"),("PUBLIC", "Public"),)
class Document(models.Model):
    user = models.ForeignKey(User)
    status=models.CharField(max_length=7,choices=choice,default="PUBLIC")
    document = models.FileField(upload_to='documents/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.document

class Comment(models.Model):
    post = models.ForeignKey('Document', related_name='comments')
    author = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    approved_comment = models.BooleanField(default=False)

    def approve(self):
        self.approved_comment = True
        self.save()

    def __str__(self):
        return self.text

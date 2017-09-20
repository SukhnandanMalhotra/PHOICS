from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db import models
import uuid
import os

def get_file_name(instance, filename):
    ext = filename.split('.')[-1]
    filename = "%s.%s" % (uuid.uuid4(), ext)
    return os.path.join('documents', filename)


choice = (("PRIVATE", "Private"),("PUBLIC", "Public"),)
class Document(models.Model):
    user = models.ForeignKey(User)
    status = models.CharField(max_length=7,choices=choice,default="PUBLIC")
    document = models.ImageField(upload_to=get_file_name,)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    # def __unicode__(self):
    #     return self.document

    # def __str__(self):
    #     return self.document

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True)
    location = models.CharField(max_length=30, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    email_confirmed = models.BooleanField(default=False)

    # def __str__(self):
    #     return self.user

# class Like(models.Model):
#     user = models.ForeignKey(User)
#     picture = models.ForeignKey(Document)
#     created = models.DateTimeField(auto_now_add=True)
#
# p = Document.objects.get()
# number_of_likes = p.like_set.all().count()


@receiver(post_save, sender=User)
def update_user_profile(sender, instance, created, **kwargs):
    # here created is a boolean that tells new instance
    #  was created or an older instance was updated.
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()



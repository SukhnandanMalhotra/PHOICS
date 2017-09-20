from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db import models
# from PIL import Image
# from io import BytesIO
# from django.core.files.uploadedfile import  InMemoryUploadedFile
# import sys

choice1 = (("PRIVATE", "Private"),("PUBLIC", "Public"),)
# choice2 = ((1,"Large"),(2, "Medium"),(3,"Small"))
# choice3 = (('horizon', "Flip Horizontally"),('vertical', "Flip Vertically"),('NONE', "None"))
# choice4 = (('clock', "Clockwise"),('anti', "Anticlockwise"), ('NONE', "None"))


class Document(models.Model):
    user = models.ForeignKey(User, default="")
    status = models.CharField(max_length=7,choices=choice1,default="PUBLIC")
    # size = models.IntegerField(choices=choice2, default=1)
    # flip = models.CharField(max_length=20, choices=choice3, default="NONE")
    # rotate = models.CharField(max_length=20, choices=choice4, default="NONE")
    document = models.FileField(upload_to='documents/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.document

    # def save(self):
    #     im=Image.open(self.document)
    #     output = BytesIO()
    #
    #     if self.size == 1:
    #         im=im.resize((700,700))
    #
    #     elif self.size == 2:
    #         im= im.resize((500,500))
    #
    #     elif self.size == 3:
    #         im=im.resize((300,300))
    #
    #     if self.flip == 'horizon':
    #         im=im.transpose(Image.FLIP_LEFT_RIGHT)
    #
    #     elif self.flip == 'vertical':
    #         im=im.transpose(Image.FLIP_TOP_BOTTOM)
    #
    #     elif self.flip == 'NONE':
    #         pass
    #
    #     if self.rotate == 'clock':
    #         im=im.rotate(270)
    #
    #     elif self.rotate == 'anti':
    #         im=im.rotate(90)
    #
    #     elif self.rotate == 'NONE':
    #         pass
    #
    #     im.save(output, format='JPEG', quality = 100)
    #     output.seek(0)
    #     self.document =InMemoryUploadedFile(output, 'ImageField', "%s.jpg" % self.document.name.split('.')[0],
    #                                         'image/jpeg', sys.getsizeof(output), None)
    #     super(Document, self).save()

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True)
    location = models.CharField(max_length=30, blank=True)
    birth_date = models.DateTimeField(null=True, blank=True)
    email_confirmed = models.BooleanField(default=False)

@receiver(post_save, sender=User)
def update_user_profile(sender, instance, created, **kwargs):
    # here created is a boolean that tells new instance
    #  was created or an older instance was updated.
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()



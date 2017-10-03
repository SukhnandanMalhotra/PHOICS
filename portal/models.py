from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db import models
import uuid
import os
from django.core.urlresolvers import reverse
from PIL import Image
from PIL import ImageFilter, ImageOps
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
import sys


def get_profile_name(instance, filename):        # to give unique id to profile pic uploaded
    ext = filename.split('.')[-1]
    filename = "%s.%s" % (uuid.uuid4(), ext)
    return os.path.join('profile_pic', filename)


class Profile(models.Model):                     # all details comming as user's profile info form get saved in this table
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    First_Name = models.CharField(max_length=100, blank=True)
    Last_Name = models.CharField(max_length=100, blank=True)
    City = models.CharField(max_length=30, blank=True)
    DOB = models.DateTimeField(null=True, blank=True)
    profile_pic = models.ImageField(upload_to=get_profile_name, default='profile_pic/default.jpg')
    email_confirmed = models.BooleanField(default=False)

    def __str__(self):                    # shows every object with a name
        return self.user.username


def get_file_name(instance, filename):               # to give unique id to images uploaded
    ext = filename.split('.')[-1]
    filename = "%s.%s" % (uuid.uuid4(), ext)
    return os.path.join('documents', filename)

choice1 = (("PRIVATE", "Private"), ("PUBLIC", "Public"),)
choice2 = ((1, "Large"), (2, "Medium"),(3, "Small"))
choice3 = (('horizon', "Flip Horizontally"), ('vertical', "Flip Vertically"),('NONE', "None"))
choice4 = (('clock', "Clockwise"), ('anti', "Anticlockwise"), ('NONE', "None"))
choice5 = (('y', 'Yes'), ('n', 'No'))
choice6 = ((1, "None"), (2, "Aqua"), (3, "Seaform"), (4, "Grayscale"), (5, "Retro"), (6, "Edges"), (7, "Negative"),(8,'Sepia'))
# choice7=((1, 'Yes'),(2,'No'))


class Document(models.Model,object):                  # all details comming about a particular picture uploaded
                                                      #  get saved in this table
    user = models.ForeignKey(User)
    status = models.CharField(max_length=7, choices=choice1, default="PUBLIC")
    size = models.IntegerField(choices=choice2, default=1)
    flip = models.CharField(max_length=17, choices=choice3, default="NONE")
    rotate = models.CharField(max_length=15, choices=choice4, default='NONE')
    blur = models.CharField(max_length=5, choices=choice5, default='n')
    effect = models.IntegerField(choices=choice6, default=1)
    document = models.ImageField(upload_to=get_file_name)
    # reset = models.IntegerField(choices=choice7, default=1)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username

    def __unicode__(self):                  # gives a common name to objects
        return self.document

    def get_absolute_url(self):
        return reverse('model_form_upload', kwargs={'pk': self.pk})

    def save(self):
        im = Image.open(self.document)    #opens a particular image
        # temp = im.copy()
        output = BytesIO()                #reads image in bytes

        # if self.reset == 1:
        #     temp.load()
        #     im = temp

        if self.size == 1:
            im = im.resize((700, 700))
        elif self.size == 2:
            im = im.resize((500, 500))
        elif self.size == 3:

            im = im.resize((300, 300))
        # im=im.resize(size,size)

        if self.flip == 'horizon':
            im = im.transpose(Image.FLIP_LEFT_RIGHT)
        elif self.flip == 'vertical':
            im = im.transpose(Image.FLIP_TOP_BOTTOM)
        elif self.flip == 'NONE':
            pass

        if self.rotate == 'clock':
            im = im.rotate(270)
        elif self.rotate == 'anti':
            im = im.rotate(90)
        elif self.rotate == 'NONE':
            pass

        if self.blur == 'y':
            im = im.filter(ImageFilter.BLUR)
        elif self.blur == 'n':
            pass

        if self.effect == 1:
            im = im.convert('RGB')
            r, g, b = im.split()
            im = Image.merge('RGB', (r, g, b))
        elif self.effect == 2:
            im = im.convert('RGB')
            r, g, b = im.split()
            im = Image.merge('RGB', (b, g, r))
        elif self.effect == 3:
            im = im.convert('RGB')
            r, g, b = im.split()
            im = Image.merge('RGB', (g, r, b))
        elif self.effect == 4:
            width, height = im.size
            for i in range(width):
                for j in range(height):
                    r,g,b = im.getpixel((i,j))
                    c=int(round((r+g+b)/3))
                    im.putpixel((i,j),(c,c,c))
        elif self.effect == 5:
            im = im.convert('RGB')
            r, g, b = im.split()
            im = Image.merge('RGB', (r, b, g))
        elif self.effect == 6:
            im = im.filter(ImageFilter.FIND_EDGES)
        elif self.effect == 7:
            im = ImageOps.invert(im)
        elif self.effect==8:
            width, height= im.size
            for i in range(width):
                for j in range(height):
                    r,g,b = im.getpixel((i,j))
                    c=int((round(r+g+b)/3))
                    R,G,B= c+100,c+100,c
                    im.putpixel((i,j),(R,G,B))


        im.save(output, format='JPEG', quality=100)
        output.seek(0)          # shows output of image saved

        self.document = InMemoryUploadedFile(output, 'ImageField', "%s.jpg" % self.document.name.split('.')[0],
                                             'image/jpeg', sys.getsizeof(output), None)
                                        # saves image in memory
        super(Document,self).save()     #saves image in database


@receiver(post_save, sender=User)
def update_user_profile(sender, instance, created, **kwargs):
    # here created is a boolean that tells new instance
    #  was created or an older instance was updated.
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()

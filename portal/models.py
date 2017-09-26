from __future__ import unicode_literals
from django.core.urlresolvers import reverse
from django.db import models
from PIL import Image
from PIL import ImageFilter

from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
import sys


choice1 = (("PRIVATE", "Private"),("PUBLIC", "Public"),)
choice2 = ((1,"Large"),(2, "Medium"),(3,"Small"))
choice3 = (('horizon',"Flip Horizontally"),('vertical',"Flip Vertically"),('NONE',"None"))
choice4 =(('clock',"Clockwise"),('anti', "Anticlockwise"),('NONE', "None"))
choice5=(('y', 'Yes'),('n','No'))
choice6=((1,'Original'),(2, 'Filter 2'),(3, 'Filter 3'),(4, 'Filter 4'), (5, 'Filter 5'),(6,'Filter 6'))
choice7=((1, 'Yes'),(2,'No'))

class Document(models.Model):
    status=models.CharField(max_length=7,choices=choice1,default="PUBLIC")
    size=models.IntegerField(choices=choice2,default=1)
    flip=models.CharField(max_length=17,choices=choice3, default="NONE")
    rotate=models.CharField(max_length=15,choices=choice4, default='NONE')
    blur=models.CharField(max_length=5,choices=choice5,default='n')
    document = models.ImageField(upload_to='documents/')
    effect=models.IntegerField(choices=choice6, default=1)
    reset = models.IntegerField(choices=choice7, default=1)
    uploaded_at = models.DateTimeField(auto_now_add=True)


    def __unicode__(self):
        return self.document

    def get_absolute_url(self):
        return reverse('model_form_upload', kwargs={'pk': self.pk})


    def save(self):

        im = Image.open(self.document)
        temp =im.copy()

        output = BytesIO()

        if self.reset == 1:
            temp.load()
            im=temp


        if self.size == 1:
            im = im.resize((700, 700))

        elif self.size == 2:
            im=im.resize((500,500))

        elif self.size == 3:
            im =im.resize((300,300))

        if self.flip =='horizon':
                im = im.transpose(Image.FLIP_LEFT_RIGHT)

        elif self.flip == 'vertical':
            im = im.transpose(Image.FLIP_TOP_BOTTOM)

        elif self.flip == 'NONE':
            pass

        if self.rotate == 'clock':
            im=im.rotate(270)

        elif self.rotate == 'anti':
            im=im.rotate(90)

        elif self.rotate == 'NONE':
            pass

        if self.blur =='y':
            im=im.filter(ImageFilter.BLUR)
        if self.blur =='n':
            pass

        if self.effect == 1:
            im=im.convert('RGB')
            r,g,b = im.split()
            im = Image.merge('RGB', (r,g,b))

        elif self.effect == 2:
            r,g,b = im.split()
            im =Image.merge('RGB', (b,g, r))

        elif self.effect == 3:
            r,g,b = im.split()
            im=Image.merge('RGB',(g,r,b))

        # elif self.effect == 4:
            # r,g,b=im.split()
            # avg= r+g+b/3
            # R,G,B =  avg, avg, avg
            # im =Image.merge('RGB', (R,G,B))
            # width, height= im.size
            # for i in im(width):
            #     for j in im(height):
            #         r, g, b = im.getpixel((i, j))
            #         avg = int(round((r + g + b) / 3.0))
            #         R, G, B = avg, avg, avg
            #         im=Image.merge(R,G, B)
            # im=im.convert('L')


        elif self.effect == 5:
            r,g,b = im.split()
            im =Image.merge('RGB', (r,b,g))

        elif self.effect ==6:
            im = im.filter(ImageFilter.FIND_EDGES)


        im.save(output, format='JPEG', quality=95)
        output.seek(0)


        self.document = InMemoryUploadedFile(output, 'ImageField', "%s.jpg" % self.document.name.split('.')[0],
                                             'image/jpeg',
                                             sys.getsizeof(output), None)
        super(Document,self).save()



































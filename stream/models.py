from django.db import models
import os
from station import settings


class UserList(models.Model):
    token = models.TextField(max_length=100)
    uid = models.TextField()

    def __str__(self):
        return self.uid


class UploadModel(models.Model):
    uid = models.IntegerField(name='uid')
    name = models.TextField(default='', name='name')
    file = models.ImageField(blank=True, null=True, name='file')

    def __str__(self):
        return self.file.path


class DownloadModel(models.Model):
    uid = models.IntegerField(name='uid')
    name = models.TextField(default='', name='name')
    file = models.ImageField(blank=True, null=True, name='file')

    def __str__(self):
        return self.file.path

    # delete overriding
    def delete(self, *args, **kwargs):
        os.remove(os.path.join(settings.MEDIA_ROOT, self.file.path))
        super(DownloadModel, self).delete(*args, **kwargs)

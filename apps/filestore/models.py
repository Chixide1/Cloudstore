from django.db import models
from django.conf import settings
# Create your models here.

class File(models.Model):
    def __str__(self) -> str:
        return str(self.name)
    
    data = models.FileField()
    name = models.CharField(max_length=200, default="")
    date_created = models.DateTimeField(auto_now_add=True)
    size = models.IntegerField(default=0)
    favourite = models.BooleanField(default=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,default=None,null=True)

class Shared(models.Model):
    def __str__(self) -> str:
        return str(self.file)
    
    url = models.URLField(null=True)
    access_count = models.IntegerField(default=0)
    file = models.ForeignKey(File, on_delete=models.CASCADE,default=None,null=True)
    


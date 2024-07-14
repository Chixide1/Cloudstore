from django.db import models
from django.conf import settings
# Create your models here.

class File(models.Model):
    def __str__(self) -> str:
        return str(self.file_name)
    
    file_data = models.FileField()
    file_name = models.CharField(max_length=200, default="")
    date_created = models.DateTimeField(auto_now_add=True)
    file_size = models.IntegerField(null=True)
    favourite = models.BooleanField(default=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,default=None,null=True)
from django.db import models

class Movies(models.Model):
    image=models.URLField(default=None,null=True,blank=True)
    title=models.CharField(max_length=250)
    date=models.DateField()
    gener=models.CharField(max_length=250)
    rating=models.FloatField(default=3.3,null=True,blank=True)
    description=models.CharField(max_length=2500)
    
    def __str__(self):
        return self.title
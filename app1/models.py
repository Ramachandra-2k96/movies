from django.db import models
from django.contrib.auth.models import User
class Movies(models.Model):
    image=models.URLField(default=None,null=True,blank=True)
    title=models.CharField(max_length=250)
    date=models.DateField()
    gener=models.CharField(max_length=250)
    rating=models.FloatField(default=3.3,null=True,blank=True)
    description=models.CharField(max_length=2500)
    
    def __str__(self):
        return self.title
class Favorites(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movies, on_delete=models.CASCADE)

    @classmethod
    def add_to_favorites(cls, user, movie):
        try:
            favorite, created = cls.objects.get_or_create(user=user, movie=movie)
            if created:
                return True  # Movie added to favorites successfully
            else:
                return False  # Movie is already in favorites
        except Exception as e:
            print(f"Error adding movie to favorites: {e}")
            return False  # Error occurred while adding movie to favorites

    
from django.db import models

# Create your models here.
class Staff(models.Model):
    code = models.CharField(max_length=15)
    name = models.CharField(max_length=30)
    rank = models.CharField(max_length=100)
    image = models.ImageField(upload_to='blog/images/%Y/%m/%d/', blank=True)

    def __str__(self):
        return f'[{self.name} {self.rank}]'
    
    def get_absolute_url(self):
        return f'{self.pk}'

    
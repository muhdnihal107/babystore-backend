from django.db import models

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=255,unique=True)
    def __str__(self):
        return self.name
    

class Product(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=10,decimal_places=2)
    image = models.URLField()
    category = models.ForeignKey(Category,on_delete=models.CASCADE,related_name='product')
    
    def __str__(self):
        return self.name


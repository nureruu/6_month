from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
class Category(models.Model):
    name = models.CharField(max_length=256)

    def __str__(self):
        return self.name

class Product(models.Model):
    title = models.CharField(max_length=300)
    description = models.TextField()
    price = models.IntegerField()
    Category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')

    def __str__(self):
        return self.title
    
class Review(models.Model):
    text = models.TextField()
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    stars = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    default = 5
    def __str__(self):
        return self.text

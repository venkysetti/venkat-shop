from django.db import models
from .category import Category

class Product(models.Model):
    name = models.CharField(max_length=30)
    cat = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    image = models.ImageField(upload_to='img', blank=True, null=True)
    desc = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name
    

    #static method to get products by id
    @staticmethod
    def get_category_id(cat_id):
        if cat_id:
            return Product.objects.filter(cat=cat_id)
        else:
            return Product.objects.all() 

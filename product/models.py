from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    # image = models.ImageField(upload_to='categories/', null=True, blank=True)

    def __str__(self):
        return self.name


class SubCategory(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='subcategories')
    name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.category.name} > {self.name}"


class Product(models.Model):
    name = models.CharField(max_length=200)
    details = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    subcategory = models.ForeignKey(SubCategory, on_delete=models.CASCADE, null=True, blank=True)
    quantity = models.IntegerField(default=0)
    bp = models.DecimalField(max_digits=10, decimal_places=2) # Buying Price
    sp = models.DecimalField(max_digits=10, decimal_places=2) # Selling Price
    # image = models.ImageField(upload_to='products/', null=True, blank=True)

    def __str__(self):
        return self.name
    
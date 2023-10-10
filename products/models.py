from django.db import models


class Brand(models.Model):
    name = models.CharField(max_length=50, unique=True)
    image = models.CharField(max_length=150)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.name)


class Product(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=80)
    brand = models.ForeignKey(Brand, related_name="products", on_delete=models.PROTECT)
    SKU = models.CharField(max_length=50, unique=True)
    price = models.IntegerField()
    image = models.CharField(max_length=150)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return str(self.name)

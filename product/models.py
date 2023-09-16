from django.db import models

class Product(models.Model):
    PRODUCT_CHOICES = [
        ('shirt', 'Shirt'),
        ('pants', 'Pants'),
        ('shoes', 'Shoes'),
        # Add more product choices as needed
    ]
    GENDER_CHOICES = [
        ('men', 'Men'),
        ('women', 'Women'),
        ('unisex', 'Unisex'),
        # Add more gender choices as needed
    ]
    SIZE_CHOICES = [
        ('s', 'S'),
        ('m', 'M'),
        ('l', 'L'),
        # Add more size choices as needed
    ]
    COLOR_CHOICES = [
        ('red', 'Red'),
        ('green', 'Green'),
        ('blue', 'Blue'),
        # Add more color choices as needed
    ]
    
    REGION_CHOICES = [
        ('A', 'Asia'),
        ('US', 'USA'),
        ('EU', 'Europe'),
        # Add more color choices as needed
    ]
    product_name = models.CharField(choices=PRODUCT_CHOICES, max_length=50, default="shirt")
    gender = models.CharField(choices=GENDER_CHOICES, max_length=10, default="men")
    size_chart = models.CharField(choices=SIZE_CHOICES, max_length=5,default="s")
    color_chart = models.CharField(choices=COLOR_CHOICES, max_length=10, default="Asia")
    region_chart = models.CharField(choices=REGION_CHOICES, max_length=10, default="red")
    fabric_description = models.TextField()
    order_no = models.CharField(max_length=50)
    other_descriptions = models.TextField()
    quantity = models.PositiveIntegerField()
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    contact_person = models.CharField(max_length=100)


    def __str__(self):
        return self.product_name

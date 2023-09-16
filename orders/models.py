from django.db import models
from django.core.exceptions import ValidationError
import datetime
def Date_validation(value):
    if value < datetime.date.today():
        raise ValidationError("The date cannot be in the past")

class Order(models.Model):
    company = models.CharField(max_length=20)
    order_no = models.CharField(max_length=20)
    order_date = models.DateField(default=datetime.date.today)
    order_delivery_status = models.CharField(max_length=20, null=True)
    delivered_on = models.DateField(null=True,validators=[Date_validation])
    cnf_no=models.CharField(null=True, max_length=50)
    def __str__(self):
        return f"Order No: {self.order_no}, Order Date: {self.order_date}"
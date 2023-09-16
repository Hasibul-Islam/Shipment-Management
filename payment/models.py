from django.db import models

class Payment(models.Model):
    order_no = models.CharField(max_length=50)
    invoice_no = models.CharField(max_length=50)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    payment_status = models.BooleanField()
    paid_date = models.DateField(null=True, blank=True, default=None)

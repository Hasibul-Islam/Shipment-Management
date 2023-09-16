from django.db import models


class CompanyDetails(models.Model):
    customer_no = models.CharField(max_length=50)
    contact_person = models.CharField(max_length=100)
    customer_company = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    street = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=50)
    email = models.EmailField()
    phone = models.CharField(max_length=50)
    best_time_to_call = models.CharField(max_length=100)

    def __str__(self):
        return self.customer_company



from django.db import models
from django.utils.translation import gettext_lazy as  _

class CNFInfo(models.Model):
    cnf_information = models.CharField(_("CNF Information"), max_length=255)
    cnf_no = models.CharField(_("CNF No"), max_length=50)
    order_no = models.CharField(_("Order no"), max_length=50, null=True, default=True)
    contact_person = models.CharField(_("Contact Person"), max_length=255)
    city = models.CharField(_("City"), max_length=255)
    country = models.CharField(_("Country"), max_length=255)
    state = models.CharField(_("State"), max_length=255)
    street = models.CharField(_("Street"), max_length=255)
    postal_code = models.CharField(_("Postal Code"), max_length=10)
    email = models.EmailField(_("Email"), max_length=255)
    phone = models.CharField(_("Phone"), max_length=20)
    best_time_to_call = models.CharField(_("Best Time to Call"), max_length=255)

    def __str__(self):
        return self.cnf_no

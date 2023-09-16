from django.db import models
from django.utils.translation import gettext_lazy as  _

class ShipmentTracking(models.Model):
    order_no = models.CharField(_("Order No"), max_length=50, null=True, default=None)
    cnf_no = models.CharField(_("CNF No"), max_length=50,null=True, default=None)
    shipment_no = models.CharField(_("Shipment No"), max_length=50,null=True, default=None)
    order_received = models.BooleanField(_("Order Received"), default=True)
    order_received_date = models.DateTimeField(null=True, default=None)
    ready = models.BooleanField(_("Ready"), default=False)
    order_ready_date = models.DateTimeField(null=True, default=None)
    carton_description = models.CharField(_("Carton Description"), max_length=255)
    shipped = models.BooleanField(_("Shipped"), default=False)
    order_shipped_date = models.DateTimeField(null=True, default=None)
    container_description = models.CharField(_("Container Description"), max_length=255)
    reached_overseas = models.BooleanField(_("Reached Overseas"), default=False)
    order_reached_overseas_date = models.DateTimeField(null=True, default=None)
    order_delivered = models.BooleanField(_("Order Delivered"), default=False)
    order_delivered_date = models.DateTimeField(null=True, default=None)
    buyer_unique_id = models.CharField(_("Buyer Unique ID"), max_length=50)
    payment_lc = models.BooleanField(_("Payment LC"), default=False)
    buyer_payment_unique_id = models.CharField(_("Buyer Payment Unique ID"), max_length=50, default="xxx")
    order_payment_lc_date= models.DateTimeField(null=True, default=None)
    def __str__(self):
        return self.order_no+"ship##"+self.cnf_no


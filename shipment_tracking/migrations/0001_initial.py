# Generated by Django 4.1.7 on 2023-04-14 14:08

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ShipmentTracking',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_no', models.CharField(default=None, max_length=50, null=True, verbose_name='Order No')),
                ('cnf_no', models.CharField(default=None, max_length=50, null=True, verbose_name='CNF No')),
                ('shipment_no', models.CharField(default=None, max_length=50, null=True, verbose_name='Shipment No')),
                ('order_received', models.BooleanField(default=True, verbose_name='Order Received')),
                ('order_received_date', models.DateTimeField(default=None, null=True)),
                ('ready', models.BooleanField(default=False, verbose_name='Ready')),
                ('order_ready_date', models.DateTimeField(default=None, null=True)),
                ('carton_description', models.CharField(max_length=255, verbose_name='Carton Description')),
                ('shipped', models.BooleanField(default=False, verbose_name='Shipped')),
                ('order_shipped_date', models.DateTimeField(default=None, null=True)),
                ('container_description', models.CharField(max_length=255, verbose_name='Container Description')),
                ('reached_overseas', models.BooleanField(default=False, verbose_name='Reached Overseas')),
                ('order_reached_overseas_date', models.DateTimeField(default=None, null=True)),
                ('order_delivered', models.BooleanField(default=False, verbose_name='Order Delivered')),
                ('order_delivered_date', models.DateTimeField(default=None, null=True)),
                ('buyer_unique_id', models.CharField(max_length=50, verbose_name='Buyer Unique ID')),
                ('payment_lc', models.BooleanField(default=False, verbose_name='Payment LC')),
                ('buyer_payment_unique_id', models.DateTimeField(default=None, null=True)),
                ('order_payment_lc_date', models.DateTimeField(default=None, null=True)),
            ],
        ),
    ]
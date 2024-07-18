from django.db import models
from django.contrib.auth.models import User

class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    stripe_customer_id = models.CharField(max_length=255, null=True, blank=True)

class Subscription(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, null=True, blank=True)
    stripe_subscription_id = models.CharField(max_length=255)
    active = models.BooleanField(default=True, null=True, blank=True)

from django.db import models
from django.contrib.auth.models import AbstractUser, User
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseForbidden


# Create your models here.

class Pharmacy(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,  # дозволяємо null для існуючих записів
        blank=True
    )
    name = models.CharField(max_length=255)
    address = models.TextField()
    contact_info = models.CharField(max_length=100)

    def __str__(self):
        return self.name





class Medicine(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,  # дозволяємо null для існуючих записів
        blank=True
    )

    pharmacy = models.ForeignKey(Pharmacy, on_delete=models.CASCADE, related_name='medicines')
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    quantity = models.PositiveIntegerField()
    expiry_date = models.DateField(blank=True, null=True)

    def __str__(self):
        return f"{self.name} ({self.pharmacy.name})"


class Equipment(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,  # дозволяємо null для існуючих записів
        blank=True
    )
    pharmacy = models.ForeignKey(Pharmacy, on_delete=models.CASCADE, related_name='equipment')
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.name} ({self.pharmacy.name})"

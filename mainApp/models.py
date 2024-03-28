from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid

class Users(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    phone_number = models.CharField(max_length=15, null=False, default='')
    address = models.CharField(max_length=200, null=False, default='')
    email = models.EmailField(max_length=100, unique=True, default='')
    pin = models.CharField(max_length=4, default='')
    username = None

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = [pin]

    def __str__(self):
        return self.first_name + " " + self.last_name

class Accounts(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user_id = models.ForeignKey(Users, on_delete=models.CASCADE, null=False)
    balance = models.IntegerField(default=0, null=False)
    date_opened = models.DateField(auto_now_add = True, null=False)
    account_type = models.CharField(max_length=50, null=False)

class Transactions(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    source = models.ForeignKey(Accounts, on_delete=models.PROTECT, null=False, related_name='source')
    destination = models.ForeignKey(Accounts, on_delete=models.PROTECT, null=False, related_name='destination')
    amount = models.IntegerField(null = False)
    timestamp = models.TimeField(auto_now_add=False)

class checkTransactions(models.Model):
    transaction = models.ForeignKey(Transactions, on_delete = models.CASCADE, null=True, related_name='transaction')
    front = models.ImageField(upload_to ='check/')
    back = models.ImageField(upload_to ='check/')

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinLengthValidator
import uuid
import random
from django.utils import timezone

class Users(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    phone_number = models.CharField(max_length=15, null=False, default='')
    address = models.CharField(max_length=200, null=False, default='')
    email = models.EmailField(max_length=100, unique=True, default='')
    pin = models.CharField(max_length=100, default='')
    date_opened = models.DateField(auto_now_add = True, null=True)

    username = None

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = [pin]

    def __str__(self):
        return self.first_name + " " + self.last_name
    
class Accounts(models.Model):
    def generateID():
        unique = False    
        while not unique:
            value = random.randint(100000000, 999999999) 
            if not Accounts.objects.filter(id = value):
                unique = True
        return value

    def __str__(self):
        return str(self.id) + " (" + self.account_type + ")" 
    
    id = models.IntegerField(primary_key=True, default = generateID)
    user_id = models.ForeignKey(Users, on_delete=models.CASCADE, null=False)
    balance = models.DecimalField(decimal_places=2, max_digits=50, default=0, null=False)
    date_opened = models.DateField(auto_now_add = True, null=False)
    account_type = models.CharField(max_length=50, null=False)
    is_deleted = models.BooleanField(default=False, editable=True)
    date_deleted = models.DateField(null=True, blank=True)

    def save(self, *args, **kwargs):
        if self.is_deleted and not self.date_deleted:
            self.date_deleted = timezone.now().date()
        elif not self.is_deleted:
            self.date_deleted = None  
        super().save(*args, **kwargs)

class Transactions(models.Model):
    source = models.ForeignKey(Accounts, on_delete=models.PROTECT, null=True, related_name='source')
    destination = models.ForeignKey(Accounts, on_delete=models.PROTECT, null=True, related_name='destination')
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    amount = models.DecimalField(max_digits=15, decimal_places=2, null = False)
    timestamp = models.DateTimeField(auto_now_add=True)
    error = models.BooleanField(default=False)

class checkTransactions(models.Model):
    transaction = models.ForeignKey(Transactions, on_delete = models.CASCADE, related_name='transaction', null = True)
    front = models.ImageField(upload_to ='check/')
    back = models.ImageField(upload_to ='check/')
    sender_info = models.CharField(max_length=100, null=False)
    spelled_amount = models.CharField(max_length=100, null=False)
    recipient_name = models.CharField(max_length=50, null=False)
    memo = models.CharField(max_length=100, null=False)
    

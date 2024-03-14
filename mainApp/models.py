from django.db import models
import uuid

class Users(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200, null=False)
    phone_number = models.CharField(max_length=15, null=False)
    address = models.CharField(max_length=200, null=False)
    email = models.EmailField(max_length=200, null=False)

    def __str__(self):
        return self.name

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

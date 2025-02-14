from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _


User = settings.AUTH_USER_MODEL

def user_directory_path(instance, filename):
    return f"user_{instance.user.id}/{filename}"

class Transaction(models.Model):
    TRANSACTION_TYPES = [
        ('Incoming Money', 'Incoming Money'),
        ('Payments', 'Payments'),
        ('Withdrawals', 'Withdrawals'),
        ('Airtime Purchase', 'Airtime Purchase'),
        ('Bank Transfer', 'Bank Transfer'),
        ('Unknown', 'Unknown'),
        ('Data Bundle Purchase', 'Data Bundle Purchase'),
        ('Bank Deposit', 'Bank Deposit'),
        ('Business Payment', 'Business Payment'),
        ('Failed Transaction', 'Failed Transaction'),
        ('Fund Transfer', 'Fund Transfer')
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    type = models.CharField(max_length=50, choices=TRANSACTION_TYPES, default='Unknown')
    sender = models.CharField(max_length=100)
    sender_id = models.CharField(max_length=50, null=True, blank=True)  # Extracted ID
    recipient = models.CharField(max_length=100)
    recipient_id = models.CharField(max_length=50, null=True, blank=True)  # Extracted ID
    amount = models.IntegerField()
    currency = models.CharField(max_length=10, default='RWF')
    transaction_id = models.CharField(max_length=100, null=True, blank=True)
    external_transaction_id = models.CharField(max_length=100, null=True, blank=True)
    date = models.DateTimeField()  # Completed date
    date_sent = models.DateTimeField()  # Sent date from SMS
    readable_date = models.CharField(max_length=100)  # Readable date as string
    service_center = models.CharField(max_length=50)
    account_balance = models.IntegerField(default=0)
    transaction_fee = models.IntegerField()
    raw_message = models.TextField()

    def __str__(self):
        return f"{self.type} - {self.amount} {self.currency} to {self.recipient}"



class TransactionData(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    file = models.FileField(upload_to=user_directory_path, blank=True, null=True)
    text_content = models.TextField(blank=True, null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
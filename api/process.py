import xml.etree.ElementTree as ET
from django.core.files.uploadedfile import InMemoryUploadedFile
from .models import Transaction
import re
from datetime import datetime
from django.utils import timezone
import os
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.conf import settings
from .models import TransactionData


def extract_transaction_details(body):
    """ Extract transaction details for Payments, Incoming Money, Bank Transfers, and Airtime Purchases """

    # Incoming Money Transaction
    if "You have received" in body and "on your mobile money account" in body:
        transaction_id = re.search(r"Financial Transaction Id:\s*(\d+)", body)
        amount = re.search(r"received ([\d,]+) RWF", body)
        sender_info = re.search(r"from (.+?) \(\*+\d+\)", body)
        completed_date = re.search(r"at (\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})", body)
        account_balance = re.search(r"Your new balance:\s*([\d,]+) RWF", body)

        return {
            "type": "Incoming Money",
            "transaction_id": transaction_id.group(1) if transaction_id else None,
            "amount": int(amount.group(1).replace(",", "")) if amount else 0,
            "sender": sender_info.group(1) if sender_info else "Unknown",
            "recipient": "User",
            "recipient_id": None,
            "completed_date": timezone.make_aware(datetime.strptime(completed_date.group(1), "%Y-%m-%d %H:%M:%S")) if completed_date else None,
            "account_balance": int(account_balance.group(1).replace(",", "")) if account_balance else 0,
            "transaction_fee": 0
        }

    # Payment Transaction
    elif "Your payment of" in body and "to" in body and "to Airtime with token" not in body:
        transaction_id = re.search(r"TxId:\s*(\d+)", body)
        amount = re.search(r"payment of ([\d,]+) RWF", body)
        recipient_info = re.search(r"to (.+?) (\d+)", body)  # Extract recipient name and ID
        completed_date = re.search(r"at (\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})", body)
        account_balance = re.search(r"Your new balance:\s*([\d,]+) RWF", body)
        transaction_fee = re.search(r"Fee was (\d+) RWF", body)

        return {
            "type": "Payments",
            "transaction_id": transaction_id.group(1) if transaction_id else None,
            "amount": int(amount.group(1).replace(",", "")) if amount else 0,
            "sender": "User",
            "recipient": recipient_info.group(1) if recipient_info else "Unknown",
            "recipient_id": recipient_info.group(2) if recipient_info else None,
            "completed_date": timezone.make_aware(datetime.strptime(completed_date.group(1), "%Y-%m-%d %H:%M:%S")) if completed_date else None,
            "account_balance": int(account_balance.group(1).replace(",", "")) if account_balance else 0,
            "transaction_fee": int(transaction_fee.group(1)) if transaction_fee else 0
        }


    # Airtime Purchase Transaction
    elif "Your payment of" in body and "to Airtime with token" in body:
        transaction_id = re.search(r"\*162\*TxId:(\d+)\*S\*", body)  # Adjusted TxId pattern
        amount = re.search(r"Your payment of ([\d,]+) RWF", body)  # Ensures correct amount extraction
        completed_date = re.search(r"at (\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})", body)
        account_balance = re.search(r"Your new balance:\s*([\d,]+) RWF", body)
        transaction_fee = re.search(r"Fee was (\d+) RWF", body)

        return {
            "type": "Airtime Purchase",
            "transaction_id": transaction_id.group(1) if transaction_id else None,
            "amount": int(amount.group(1).replace(",", "")) if amount else 0,
            "sender": "User",
            "recipient": "Airtime",
            "recipient_id": None,
            "completed_date": timezone.make_aware(datetime.strptime(completed_date.group(1), "%Y-%m-%d %H:%M:%S")) if completed_date else None,
            "account_balance": int(account_balance.group(1).replace(",", "")) if account_balance else 0,
            "transaction_fee": int(transaction_fee.group(1)) if transaction_fee else 0
        }


    # Bank Transfer Transaction
    elif "transferred to" in body and "Fee was:" in body:
        transaction_id = None  # No transaction ID in the example provided
        amount = re.search(r"\*165\*S\*([\d,]+) RWF transferred", body)
        recipient_info = re.search(r"to (.+?) \((\d+)\)", body)  # Extract recipient name and ID
        sender_info = re.search(r"from (\d+)", body)  # Extract sender ID
        completed_date = re.search(r"at (\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})", body)
        account_balance = re.search(r"New balance:\s*([\d,]+) RWF", body)
        transaction_fee = re.search(r"Fee was:\s*(\d+) RWF", body)

        return {
            "type": "Bank Transfer",
            "transaction_id": transaction_id,
            "amount": int(amount.group(1).replace(",", "")) if amount else 0,
            "sender": "User",
            "sender_id": sender_info.group(1) if sender_info else None,
            "recipient": recipient_info.group(1) if recipient_info else "Unknown",
            "recipient_id": recipient_info.group(2) if recipient_info else None,
            "completed_date": timezone.make_aware(datetime.strptime(completed_date.group(1), "%Y-%m-%d %H:%M:%S")) if completed_date else None,
            "account_balance": int(account_balance.group(1).replace(",", "")) if account_balance else 0,
            "transaction_fee": int(transaction_fee.group(1)) if transaction_fee else 0
        }
    
    # Withdrawal
    elif "withdrawn" in body:
        transaction_id = re.search(r"Financial Transaction Id:\s*(\d+)", body)
        amount = re.search(r"withdrawn ([\d,]+) RWF", body)
        agent_info = re.search(r"via agent: (.+?) \((\d+)\)", body)
        completed_date = re.search(r"at (\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})", body)
        account_balance = re.search(r"Your new balance:\s*([\d,]+) RWF", body)
        transaction_fee = re.search(r"Fee paid:\s*(\d+) RWF", body)
        sender_id = re.search(r"mobile money account:\s*(\d+)", body)  # Extract sender ID

        return {
            "type": "Withdrawals",
            "transaction_id": transaction_id.group(1) if transaction_id else None,
            "amount": int(amount.group(1)) if amount else 0,
            "sender": "User",
            "sender_id": sender_id.group(1) if sender_id else None,  # Use sender_id extracted from the message
            "recipient": agent_info.group(1) if agent_info else "Unknown",
            "recipient_id": agent_info.group(2) if agent_info else None,  # Ensure recipient_id is extracted
            "completed_date": timezone.make_aware(datetime.strptime(completed_date.group(1), "%Y-%m-%d %H:%M:%S")) if completed_date else None,
            "account_balance": int(account_balance.group(1).replace(",", "")) if account_balance else 0,
            "transaction_fee": int(transaction_fee.group(1)) if transaction_fee else 0
        }
        
        
    # Data Bundle Purchase Transaction
    elif "by Data Bundle" in body:
        amount = re.search(r"A transaction of ([\d,]+) RWF", body)
        completed_date = re.search(r"at (\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})", body)
        account_balance = re.search(r"Your new balance:([\d,]+) RWF", body)
        transaction_id = re.search(r"Financial Transaction Id: (\d+)", body)
        external_transaction_id = re.search(r"External Transaction Id: (\d+)", body)
        transaction_fee = re.search(r"Fee was (\d+) RWF", body)

        return {
            "type": "Data Bundle Purchase",
            "transaction_id": transaction_id.group(1) if transaction_id else None,
            "external_transaction_id": external_transaction_id.group(1) if external_transaction_id else None,
            "amount": int(amount.group(1).replace(",", "")) if amount else 0,
            "sender": "User",
            "recipient": "Data Bundle MTN",
            "recipient_id": None,
            "completed_date": timezone.make_aware(datetime.strptime(completed_date.group(1), "%Y-%m-%d %H:%M:%S")) if completed_date else None,
            "account_balance": int(account_balance.group(1).replace(",", "")) if account_balance else 0,
            "transaction_fee": int(transaction_fee.group(1)) if transaction_fee else 0
        }
        
    # Bank Deposit Transaction
    elif "A bank deposit of" in body:
        amount = re.search(r"A bank deposit of ([\d,]+) RWF", body)
        completed_date = re.search(r"at (\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})", body)
        account_balance = re.search(r"Your NEW BALANCE :([\d,]+) RWF", body)
        transaction_id = re.search(r"Cash Deposit::CASH::::0::(\d+)", body)  # Extracts the deposit transaction ID

        return {
            "type": "Bank Deposit",
            "transaction_id": transaction_id.group(1) if transaction_id else None,
            "amount": int(amount.group(1).replace(",", "")) if amount else 0,
            "sender": "Bank",
            "recipient": "User",
            "recipient_id": None,
            "completed_date": timezone.make_aware(datetime.strptime(completed_date.group(1), "%Y-%m-%d %H:%M:%S")) if completed_date else None,
            "account_balance": int(account_balance.group(1).replace(",", "")) if account_balance else 0,
            "transaction_fee": 0  # Deposits usually don't have a fee
        }
        
    # Business Payment Transaction
    elif "A transaction of" in body and "on your MOMO account was successfully completed" in body:
        amount = re.search(r"A transaction of ([\d,]+) RWF", body)
        recipient_info = re.search(r"by (.+?) on your MOMO account", body)  # Extract business name
        completed_date = re.search(r"at (\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})", body)
        account_balance = re.search(r"Your new balance:([\d,]+) RWF", body)
        transaction_id = re.search(r"Financial Transaction Id: (\d+)", body)
        external_transaction_id = re.search(r"External Transaction Id: ([\w-]+)", body)
        transaction_fee = re.search(r"Fee was (\d+) RWF", body)

        return {
            "type": "Business Payment",
            "transaction_id": transaction_id.group(1) if transaction_id else None,
            "external_transaction_id": external_transaction_id.group(1) if external_transaction_id else None,
            "amount": int(amount.group(1).replace(",", "")) if amount else 0,
            "sender": "User",
            "recipient": recipient_info.group(1) if recipient_info else "Unknown Business",
            "recipient_id": None,
            "completed_date": timezone.make_aware(datetime.strptime(completed_date.group(1), "%Y-%m-%d %H:%M:%S")) if completed_date else None,
            "account_balance": int(account_balance.group(1).replace(",", "")) if account_balance else 0,
            "transaction_fee": int(transaction_fee.group(1)) if transaction_fee else 0
        }
        
    # Failed Transaction
    elif "failed at" in body:
        amount = re.search(r"the transaction with amount ([\d,]+) RWF", body)
        reason = re.search(r"message:\s*(.*?)\s*failed", body)  # Extract failure reason if available
        failed_date = re.search(r"failed at (\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})", body)

        return {
            "type": "Failed Transaction",
            "transaction_id": None,  # No transaction ID for failed transactions
            "amount": int(amount.group(1).replace(",", "")) if amount else 0,
            "sender": "User",
            "recipient": "Unknown",  # No recipient since transaction failed
            "recipient_id": None,
            "failed_date": timezone.make_aware(datetime.strptime(failed_date.group(1), "%Y-%m-%d %H:%M:%S")) if failed_date else None,
            "reason": reason.group(1) if reason else "Unknown",
            "status": "Failed",
            "account_balance": 0
        }

    # Fund Transfer (Mobile Money to Bank or Another User)
    elif "You have transferred" in body and "from your mobile money account" in body:
        transaction_id = re.search(r"Financial Transaction Id:\s*(\d+)", body)
        amount = re.search(r"You have transferred ([\d,]+) RWF", body)
        sender_account = re.search(r"from your mobile money account (\d+)", body)
        recipient_info = re.search(r"to (.+?) \((\d+)\)", body)  # Extract recipient name and phone number
        completed_date = re.search(r"at (\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})", body)
        account_balance = re.search(r"Your new balance:\s*([\d,]+) RWF", body)

        return {
            "type": "Fund Transfer",
            "transaction_id": transaction_id.group(1) if transaction_id else None,
            "amount": int(amount.group(1).replace(",", "")) if amount else 0,
            "sender": "User",
            "sender_account": sender_account.group(1) if sender_account else "Unknown",
            "recipient": recipient_info.group(1) if recipient_info else "Unknown",
            "recipient_id": recipient_info.group(2) if recipient_info else None,
            "completed_date": timezone.make_aware(datetime.strptime(completed_date.group(1), "%Y-%m-%d %H:%M:%S")) if completed_date else None,
            "account_balance": int(account_balance.group(1).replace(",", "")) if account_balance else 0,
        }


    # Unknown transaction type
    return {"type": "Unknown"}


def extract_sms_body(root, request):
    for sms in root.findall("sms"):
        body = sms.get("body", "")
        transaction_data = extract_transaction_details(body)

        # Convert timestamps
        
        date_timestamp = int(sms.get("date", 0)) // 1000
        date_sent_timestamp = int(sms.get("date_sent", 0)) // 1000
        date = timezone.make_aware(datetime.fromtimestamp(date_timestamp))
        date_sent = timezone.make_aware(datetime.fromtimestamp(date_sent_timestamp))

        # Determine transaction type
        transaction_type = transaction_data["type"] if transaction_data else "Unknown"

        # Save transaction to database
        if transaction_data:
            Transaction.objects.create(
                user = request.user,
                type=transaction_type,
                sender=transaction_data.get("sender", sms.get("address", "Unknown")),
                sender_id=transaction_data.get("sender_id"),
                recipient=transaction_data.get("recipient", "Unknown"),
                recipient_id=transaction_data.get("recipient_id"),
                amount=transaction_data.get("amount", 0),
                transaction_id=transaction_data.get("transaction_id"),
                date=transaction_data["completed_date"] if transaction_data.get("completed_date") else date,  # Handle missing completed_date
                date_sent=date_sent,
                readable_date=sms.get("readable_date", ""),
                service_center=sms.get("service_center", ""),
                account_balance=transaction_data.get("account_balance", 0),
                transaction_fee=transaction_data.get("transaction_fee", 0),
                raw_message=body
            )
    


def save_transaction_data(user, file=None, text=None):
    """
    Save XML file to the user's directory and/or store text in the database.
    If only text is provided, it also creates an XML file.
    """
    transaction = TransactionData(user=user)

    # Create user directory
    user_folder = f"user_{user.id}"
    save_path = os.path.join(settings.MEDIA_ROOT, user_folder)
    os.makedirs(save_path, exist_ok=True)  # Ensure the directory exists

    # Handle file upload
    if file:
        file_path = os.path.join(save_path, file.name)

        # Save the file to storage
        with default_storage.open(file_path, 'wb+') as destination:
            for chunk in file.chunks():
                destination.write(chunk)

        # Read file content and store it as text
        with open(file_path, "r", encoding="utf-8") as f:
            text_content = f.read()

        transaction.file.name = f"{user_folder}/{file.name}"
        transaction.text_content = text_content  # Save extracted text

    # Handle pasted text and create a file if only text is given
    if text:
        transaction.text_content = text  # Save text content

        # Create an XML file from text
        file_name = f"user_{user.id}_transactions.xml"
        file_path = os.path.join(save_path, file_name)

        with open(file_path, "w", encoding="utf-8") as f:
            f.write(text)  # Save text as XML file

        transaction.file.name = f"{user_folder}/{file_name}"  # Save file reference

    transaction.save()
    return transaction



def process_pasted_text(pasted_text: str, request):
    try:
        root = ET.fromstring(pasted_text)
        extract_sms_body(root, request)
        
        # Save to database
        save_transaction_data(request, text=pasted_text)

    except Exception as e:
        print(f"Error: {e}")


def process_uploaded_file(uploaded_file, request):
    try:
        tree = ET.parse(uploaded_file)
        root = tree.getroot()
        extract_sms_body(root, request)

        # Save to database
        save_transaction_data(user=request.user, file=uploaded_file)

        print(f"Transactions imported successfully!")

    except Exception as e:
        print(f"Error: {e}")

from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponse
import csv
import json
from django.contrib import messages
from django.urls import reverse
from .models import Transaction
from django.template.loader import get_template
from django.http import HttpResponseRedirect
from weasyprint import HTML
import tempfile


@login_required
def details_download(request, type, id, file_format):
    """Download transaction details as JSON, CSV, or PDF."""
    transaction = get_object_or_404(Transaction, user=request.user, id=id, type=type)
             
    transaction_data = {
        "id": transaction.id,
        "type": transaction.type,
        "sender": transaction.sender,
        "recipient": transaction.recipient,
        "amount": transaction.amount,
        "currency": transaction.currency,
        "transaction_id": transaction.transaction_id,
        "date": transaction.date.strftime("%Y-%m-%d %H:%M:%S"),
        "service_center": transaction.service_center,
        "account_balance": transaction.account_balance,
        "transaction_fee": transaction.transaction_fee,
        "raw_message": transaction.raw_message,
    }

    # Handle the file download logic directly
    if file_format == "json":
        filename = f'{type}_{id}.json'
        response = HttpResponse(json.dumps(transaction_data, indent=4), content_type="application/json")
        response["Content-Disposition"] = f'attachment; filename="{filename}"'
    
    elif file_format == "csv":
        filename = f'{type}_{id}.csv'
        response = HttpResponse(content_type="text/csv")
        response["Content-Disposition"] = f'attachment; filename="{filename}"'
        
        writer = csv.writer(response)
        writer.writerow(transaction_data.keys())  # Write header
        writer.writerow(transaction_data.values())  # Write data
    
    elif file_format == "pdf":
        # Your logic for generating PDF (WeasyPrint)
        template = get_template("api/details.html")  # Use your actual details template
        html_content = template.render({"details": transaction})

        # Create a PDF file
        filename = f'transaction_{id}.pdf'
        response = HttpResponse(content_type="application/pdf")
        response["Content-Disposition"] = f'attachment; filename="{filename}"'

        # Use WeasyPrint to generate the PDF
        HTML(string=html_content).write_pdf(response)

    else:
        messages.error(request, "Invalid file format.")
        return redirect(request.get_full_path())

    # Set success message before triggering the download
    messages.success(request, "Your file download will begin shortly...")

    # Instead of rendering a download trigger page, redirect to a separate success page
    return redirect('api:download_success', type=type, id=id, file_format=file_format)

@login_required
def transaction_download(request):
    """Download transaction details as JSON, CSV, or PDF."""
    file_format = request.GET["file_format"]

    # Get all transactions for the logged-in user
    transactions = Transaction.objects.filter(user=request.user)
    
    # Prepare the transaction data
    transaction_data = [
        {
            "id": transaction.id,
            "type": transaction.type,
            "sender": transaction.sender,
            "recipient": transaction.recipient,
            "amount": transaction.amount,
            "currency": transaction.currency,
            "transaction_id": transaction.transaction_id,
            "date": transaction.date.strftime("%Y-%m-%d %H:%M:%S"),
            "service_center": transaction.service_center,
            "account_balance": transaction.account_balance,
            "transaction_fee": transaction.transaction_fee,
            "raw_message": transaction.raw_message,
        }
        for transaction in transactions
    ]

    # Handle the file download based on the file_format selected
    if file_format == "json":
        filename = 'transactions.json'
        response = HttpResponse(json.dumps(transaction_data, indent=4), content_type="application/json")
        response["Content-Disposition"] = f'attachment; filename="{filename}"'
    
    elif file_format == "csv":
        filename = 'transactions.csv'
        response = HttpResponse(content_type="text/csv")
        response["Content-Disposition"] = f'attachment; filename="{filename}"'
        
        writer = csv.writer(response)
        # Write header
        writer.writerow(transaction_data[0].keys())
        # Write data for each transaction
        for data in transaction_data:
            writer.writerow(data.values())
    
    else:
        messages.error(request, "Invalid file format.")
        return redirect(request.META.get('HTTP_REFERER'))  # Redirect back to the previous page if error
    
    return response



@login_required
def download_success(request, type, id, file_format):
    # The view to handle the success page and display the message
    return render(request, 'api/download_success.html', {
        'message': 'Your file download is starting...',
        'type': type,
        'id': id,
        'file_format': file_format
    })

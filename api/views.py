from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Transaction
from .forms import TransactionUploadForm  # Ensure this import is correct
from .process import process_pasted_text, process_uploaded_file
from collections import Counter
from django.utils.timezone import now
import json
from collections import defaultdict
from .plots import index_transactions, bar_chart, donut_chart,pie_chart,line_chart,histogram_chart,scatter_chart
from .forms import TransactionUploadForm
from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render


@login_required
def upload_file(request):
    if request.method == "POST":
        form = TransactionUploadForm(request.POST, request.FILES)
        
        if form.is_valid():
            file = request.FILES.get('file')
            text = form.cleaned_data.get('text')

            # Remove the previous SMS data (if any)
            Transaction.objects.filter(user=request.user).delete()  # Deletes all previous SMS data

            if file:
                process_uploaded_file(file, request)
            elif text:
                process_pasted_text(text, request)

            messages.success(request, "Your data has been successfully updated.")
            return redirect('userauths:my_profile')
        else:
            messages.error(request, "There was an error processing your request. Please check the form.")
    else:
        form = TransactionUploadForm()

    context = {
        'form': form,
    }
    return render(request, 'userauths/profile.html', context)

@login_required
def index(request):
    
    transactions, transaction_summary = index_transactions(request)
        
    bar_chart_data = bar_chart(request)
    donut_chart_data = donut_chart(request)
    pie_chart_data = pie_chart(request)
    formatted_trends, all_types = line_chart(request)
    histogram_data = histogram_chart(request)
    scatter_chart_data = scatter_chart(request)
    

    
    if request.method == "POST":
        form = TransactionUploadForm(request.POST, request.FILES)
        
        if form.is_valid():
            file = request.FILES.get('file')
            text = form.cleaned_data.get('text')

            if file:
                process_uploaded_file(file, request)
            elif text:
                process_pasted_text(text, request)

            return redirect('api:index')

    else:
        form = TransactionUploadForm()
    
    context = {
        'transactions': transactions,
        'transaction_summary': transaction_summary,
        "form": form,
        'bar_chart_data_json': json.dumps(bar_chart_data),  # Bar Chart Data
        'donut_chart_data_json': json.dumps(donut_chart_data),  # Donut Chart Data
        'pie_chart_data_json': json.dumps(pie_chart_data),
        'line_chart_data_json': json.dumps(formatted_trends),
        'line_chart_labels_json': json.dumps(list(all_types)),
        'apex_histogram_data_json': json.dumps(histogram_data),  # Convert to JSON for ApexCharts
        'apex_scatter_data_json': json.dumps(scatter_chart_data),  # Convert to JSON for ApexCharts
    }

    return render(request, 'api/index.html', context)


def get_transactions(user, type=None):
    """Helper function to get user transactions based on type."""
    if type == "All Transactions" or type is None:
        return Transaction.objects.filter(user=user)
    return Transaction.objects.filter(user=user, type=type)

@login_required
def transaction(request, type):
    """Render transactions page."""
    transactions, transaction_summary = index_transactions(request)
    payments = get_transactions(request.user, type)

    context = {
        "payments": payments,
        "type": type,
        "transactions": transactions,
        "transaction_summary": transaction_summary,
    }
    
    return render(request, "api/transaction.html", context)

@login_required
def details(request, type, id):
    """Render transaction details page."""
    details = get_object_or_404(Transaction, user=request.user, id=id, type=type)

    context = {"details": details}
    return render(request, "api/details.html", context)

@login_required
def transaction_api(request, type):
    """Return transactions as JSON."""
    payments = get_transactions(request.user, type)
    transactions_list = list(payments.values())  # Convert QuerySet to list of dicts

    return JsonResponse({"transactions": transactions_list}, safe=False)

@login_required
def details_api(request, type, id):
    """Return transaction details as JSON."""
    details = get_object_or_404(Transaction, user=request.user, id=id, type=type)

    transaction_data = {
        "id": details.id,
        "type": details.type,
        "sender": details.sender,
        "recipient": details.recipient,
        "amount": details.amount,
        "currency": details.currency,
        "transaction_id": details.transaction_id,
        "date": details.date.strftime("%Y-%m-%d %H:%M:%S"),
        "service_center": details.service_center,
        "account_balance": details.account_balance,
        "transaction_fee": details.transaction_fee,
        "raw_message": details.raw_message,
    }

    return JsonResponse({"transaction_details": transaction_data})



# Errors
def error_view(request, exception=None, status=500):
    """A single view to handle 404, 500, 403, and 400 errors dynamically."""
    context = {
        "status_code": status,
        "message": {
            404: "Page Not Found",
            500: "Internal Server Error",
            403: "Forbidden Access",
            400: "Bad Request"
        }.get(status, "An Error Occurred"),
    }
    return render(request, "errors/error.html", context, status=status)
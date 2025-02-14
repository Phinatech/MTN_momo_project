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


@login_required
def transaction(request, type):
    transactions, transaction_summary = index_transactions(request)
    if type == "All Transactions":
        payments = Transaction.objects.filter(user=request.user).all()
    else:
        payments = Transaction.objects.filter(user=request.user, type=type)

    context = {
        "payments": payments,
        "type": type,
        'transactions': transactions,
        'transaction_summary': transaction_summary,
        
    }
    
    return render(request, 'api/transaction.html', context)

@login_required
def details(request, type, id):

    details = Transaction.objects.get(user=request.user, id=id, type=type)

    context = {
        "details": details,
    }
    
    return render(request, 'api/details.html', context)




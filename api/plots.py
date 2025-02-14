from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Transaction
from collections import Counter
from django.utils.timezone import now
from collections import defaultdict
from django.db import models

def get_user_transactions(request):
    """Fetch all transactions for the current user."""
    transactions = Transaction.objects.filter(user=request.user)
    
    # Count occurrences of each transaction type (for Donut Chart)
    transaction_counts = dict(Counter(transactions.values_list('type', flat=True)))
    total_transactions = sum(transaction_counts.values())
    
    return transactions, transaction_counts, total_transactions 


def index_transactions(request):
    transactions, _, total_transactions = get_user_transactions(request)
    
    # Define icons and colors for each transaction type
    transaction_styles = {
        'Incoming Money': {'icon': 'fas fa-money-bill-wave', 'color': 'bg-success'},
        'Payments': {'icon': 'fas fa-credit-card', 'color': 'bg-primary'},
        'Withdrawals': {'icon': 'fas fa-wallet', 'color': 'bg-danger'},
        'Airtime Purchase': {'icon': 'fas fa-mobile-alt', 'color': 'bg-warning'},
        'Bank Transfer': {'icon': 'fas fa-university', 'color': 'bg-info'},
        'Unknown': {'icon': 'fas fa-question-circle', 'color': 'bg-secondary'},
        'Data Bundle Purchase': {'icon': 'fas fa-wifi', 'color': 'bg-dark'},
        'Bank Deposit': {'icon': 'fas fa-piggy-bank', 'color': 'bg-success'},
        'Business Payment': {'icon': 'fas fa-handshake', 'color': 'bg-primary'},
        'Failed Transaction': {'icon': 'fas fa-times-circle', 'color': 'bg-danger'},
        'Fund Transfer': {'icon': 'fas fa-exchange-alt', 'color': 'bg-info'},
    }

    # List to hold transaction summaries
    transaction_summary = []

    # Add the "All Transactions" column first
    total_amount = transactions.aggregate(total=models.Sum('amount'))['total'] or 0
    transaction_summary.append({
        'type': 'All Transactions',
        'count': total_transactions,
        'total_amount': total_amount,
        'percentage': 100,
        'icon': 'fas fa-list',
        'color': 'bg-dark',
    })

    # Adding individual transaction types 
    for transaction_type, _ in Transaction.TRANSACTION_TYPES:
        filtered_transactions = transactions.filter(type=transaction_type)
        count = filtered_transactions.count()
        total_amount = filtered_transactions.aggregate(total=models.Sum('amount'))['total'] or 0
        percentage = (count / total_transactions) * 100 if total_transactions > 0 else 0

        transaction_summary.append({
            'type': transaction_type,
            'count': count,
            'total_amount': total_amount,
            'percentage': round(percentage, 2),
            'icon': transaction_styles.get(transaction_type, {}).get('icon', 'fas fa-circle'),
            'color': transaction_styles.get(transaction_type, {}).get('color', 'bg-secondary'),
        })

    return transactions, transaction_summary


def bar_chart(request):
    
    transactions, _, _ = get_user_transactions(request)

    # Grouping transactions by type (for Bar Chart)
    transaction_summary = defaultdict(lambda: {"amount": 0, "fee": 0, "balance": 0})

    for tx in transactions:
        transaction_summary[tx.type]["amount"] += tx.amount
        transaction_summary[tx.type]["fee"] += tx.transaction_fee
        transaction_summary[tx.type]["balance"] += tx.account_balance

    # Converting  to list for JSON for better visualization
    bar_chart_data = [
        {
            "label": key,
            "amount": value["amount"],
            "fee": value["fee"],
            "balance": value["balance"],
        }
        for key, value in transaction_summary.items()
    ]
    
    return bar_chart_data


def donut_chart(request):
    
    _, transaction_counts, total_transactions = get_user_transactions(request)
    
    # Preparing Donut Chart Data
    donut_chart_data = [
        {
            "label": key,
            "count": value,
            "percentage": round((value / total_transactions) * 100, 2)
        }
        for key, value in transaction_counts.items()
    ]
    
    return donut_chart_data


def pie_chart(request):
    _, transaction_counts, total_transactions = get_user_transactions(request)
        
    # Compute percentage of each transaction type
    pie_chart_data = {
        "labels": list(transaction_counts.keys()),
        "values": [round((count / total_transactions) * 100, 2) for count in transaction_counts.values()]
    }
    
    return pie_chart_data
    
def line_chart(request):
    
    transactions, _, _ = get_user_transactions(request)
      
    # Dictionary to hold transaction trends
    transaction_trends = defaultdict(lambda: defaultdict(float))

    # Aggregate data by date and transaction type
    for tx in transactions:
        date_str = tx.date.strftime("%Y-%m-%d")  # Format date as string (YYYY-MM-DD)
        transaction_trends[date_str][tx.type] += tx.amount

    # Convert data to list format for JSON
    formatted_trends = []
    all_types = set()

    for date, types in sorted(transaction_trends.items()):
        entry = {"date": date}
        for t_type, amount in types.items():
            entry[t_type] = amount
            all_types.add(t_type)
        formatted_trends.append(entry)

    # Ensure all transaction types are present in each entry
    for entry in formatted_trends:
        for t_type in all_types:
            entry.setdefault(t_type, 0)  # Default missing types to 0

    return formatted_trends, all_types


def histogram_chart(request):
    
    transactions, _, _ = get_user_transactions(request)
    
    # Extract transaction amounts
    amounts = [tx.amount for tx in transactions]

    # Create bins (group transaction amounts into ranges)
    bin_size = 10000  # Adjust bin size as needed
    bins = Counter((amount // bin_size) * bin_size for amount in amounts)

    # Convert to Apex format
    histogram_data = {
        "categories": [str(bin_range) for bin_range in sorted(bins.keys())],  # X-axis (bins)
        "series": [{"name": "Transactions", "data": [bins[bin_range] for bin_range in sorted(bins.keys())]}]  # Y-axis (counts)
    }
    
    return histogram_data

def scatter_chart(request):

    transactions, _, _ = get_user_transactions(request)

    # Extract transaction amount, fee, and type for tooltips
    scatter_data = [
        {"x": tx.amount, "y": tx.transaction_fee, "type": tx.type} for tx in transactions
    ]

    # Convert to JSON for ApexCharts
    scatter_chart_data = {
        "series": [
            {
                "name": "Transaction Fees",
                "data": scatter_data
            }
        ]
    }
    
    return scatter_chart_data
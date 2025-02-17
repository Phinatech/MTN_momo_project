from .models import Transaction
from datetime import date, timedelta
from userauths.models import Profile

def my_context_processors(request):
    try:
        # Define icons and colors for each transaction type
        transaction_styles = {
            'Incoming Money': {'icon': 'dollar-sign', 'color': 'bg-success'},
            'Payments': {'icon': 'credit-card', 'color': 'bg-primary'},
            'Withdrawals': {'icon': 'arrow-down-circle', 'color': 'bg-danger'},
            'Airtime Purchase': {'icon': 'smartphone', 'color': 'bg-warning'},
            'Bank Transfer': {'icon': 'send', 'color': 'bg-info'},
            'Unknown': {'icon': 'help-circle', 'color': 'bg-secondary'},
            'Data Bundle Purchase': {'icon': 'wifi', 'color': 'bg-dark'},
            'Bank Deposit': {'icon': 'database', 'color': 'bg-success'},
            'Business Payment': {'icon': 'briefcase', 'color': 'bg-primary'},
            'Failed Transaction': {'icon': 'x-circle', 'color': 'bg-danger'},
            'Fund Transfer': {'icon': 'repeat', 'color': 'bg-info'},
        }

        # An empty List to hold transaction summaries
        transaction_sidebar = []
        # Get the current user's profile
        profile = Profile.objects.get(user=request.user)
        
        # Get the current date and subtract 30 days
        start_date = date.today() - timedelta(days=30)
        
        # Add individual transaction types
        for transaction_type, _ in Transaction.TRANSACTION_TYPES:

            transaction_sidebar.append({
                'type': transaction_type,
                'icon': transaction_styles.get(transaction_type, {}).get('icon', 'fas fa-circle'),
                'color': transaction_styles.get(transaction_type, {}).get('color', 'bg-secondary'),
            })


    except Exception as e:
        transaction_sidebar = None
    
    
    return {
        "transaction_sidebar": transaction_sidebar,
        }

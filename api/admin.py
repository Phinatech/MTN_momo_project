from django.contrib import admin
from .models import Transaction, TransactionData
from import_export.admin import ImportExportModelAdmin

@admin.register(Transaction)
class TransactionAdmin(ImportExportModelAdmin):
    list_display = ('type', 'sender', 'amount', 'date', 'transaction_id')
    search_fields = ('sender', 'transaction_id')
    list_filter = ('type', 'date')
    
    
@admin.register(TransactionData)
class TransactionDataAdmin(ImportExportModelAdmin):
    list_display = ('user', 'file', 'uploaded_at')
    search_fields = ('user', 'file')
    list_filter = ('user', 'file', 'uploaded_at')


from django.urls import path
from api import views
from .downloads import details_download, download_success, transaction_download


app_name = "api"

urlpatterns = [
    path("", views.index, name="index"),
    path("upload_file/", views.upload_file, name="upload_file"),
    path("download/", transaction_download, name="transaction_download"),
    path("download/<str:type>/<int:id>/<str:file_format>/", details_download, name="details_download"),
    
    path('download/success/<str:type>/<int:id>/<str:file_format>/', download_success, name='download_success'),
    
    path('transaction/<str:type>/', views.transaction, name='transaction'),
    
    # Details
    path('<str:type>/details/<int:id>/', views.details, name='details'),

    path("api/transaction/<str:type>/", views.transaction_api, name="transaction_api"),
    path("api/details/<str:type>/<int:id>/", views.details_api, name="details_api"),
]


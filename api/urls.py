from django.urls import path
from api import views

app_name = "api"

urlpatterns = [
    path("", views.index, name="index"),
    path("upload_file/", views.upload_file, name="upload_file"),
    
    path('transaction/<str:type>/', views.transaction, name='transaction'),
    
    # Details
    path('<str:type>/details/<int:id>/', views.details, name='details'),
    
]

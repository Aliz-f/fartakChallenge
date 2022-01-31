from django.urls import path
from .views import contactlist, contactDetail

urlpatterns = [
    path('',contactlist.as_view()),
    path('get/<int:id>', contactDetail.as_view()),
    
]
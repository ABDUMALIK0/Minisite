from django.urls import path
from .views import index, name_card, name_card2, list

urlpatterns = [
    path('', index),
    path('list/', list),
    path('name_card/<int:pk>/', name_card),
    path('name_card2/<int:pk>/', name_card2),
]
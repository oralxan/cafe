from django.urls import path
from .views import home, menu, contact, reviews
from . import views


urlpatterns = [
    path('', home, name='home'),
    path('menu/', menu, name='menu'),
    path('contact/', contact, name='contact'),
    path('reviews/', reviews, name='reviews'), 
    path('add-to-order/', views.add_to_order, name='add_to_order'),
    path('save-customer-info/', views.save_customer_info, name='save_customer_info'),
    path('orders/', views.orders_view, name='orders'),
     path('delete-order/', views.delete_order, name='delete_order'),
]



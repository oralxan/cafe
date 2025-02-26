from django.contrib import admin
from .models import Category, MenuItem, Review, Order, OrderItem


admin.site.register(Category)
admin.site.register(MenuItem)
admin.site.register(Review)
admin.site.register(Order)
admin.site.register(OrderItem)

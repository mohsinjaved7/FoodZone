from django.contrib import admin
from . models import *

admin.site.site_header = "FoodZone | Admin "

class DishAdmin(admin.ModelAdmin):
    list_display = ['id','name','price','added_on','updated_on']

class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id','name','added_on','updated_on']

class ContactAdmin(admin.ModelAdmin):
    list_display = ['id','name','email','subject','message','added_to','is_approved']

class BookingAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'contact', 'date', 'guests']
# Register your models here.


admin.site.register(Contact, ContactAdmin)
admin.site.register(Profile)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Dish, DishAdmin)
admin.site.register(Team)
admin.site.register(Order)
admin.site.register(Booking_table,BookingAdmin)
admin.site.register(Sub_category)

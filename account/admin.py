from django.contrib import admin
from .models import contact
from .models import CustomUser,Customer
# Register your models here.

# Register your models here.
class ContactAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'subject', 'created_at')  
    search_fields = ('name', 'email', 'subject')  
    list_filter = ('created_at',)  
    ordering = ('-created_at',)  

admin.site.register(contact, ContactAdmin)

class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'first_name', 'last_name', 'email', 'contact','is_staff','is_active')
    ordering = ('username',)

class CustomerAdmin(admin.ModelAdmin):
    list_display = ('username', 'first_name', 'last_name', 'email', 'contact','dob','gender','profile_picture')
    ordering = ('username',)
    
admin.site.register(CustomUser, UserAdmin)

admin.site.register(Customer, CustomerAdmin)
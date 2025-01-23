from django.contrib import admin
from .models import Category, Product, ShippingAddress, Order, OrderItem,ProductWeightPrice,Cart,Invoice

# Register your models here.
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)
class ProductWeightPriceInline(admin.TabularInline): 
    model = ProductWeightPrice
    extra = 1  
    fields = ('weight', 'price') 

# Register the Product model with the inline
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'category', 'stock_qty', 'created_at', 'updated_at')
    search_fields = ('title', 'category__name')
    list_filter = ('category', 'created_at')
    readonly_fields = ('created_at', 'updated_at')
    inlines = [ProductWeightPriceInline]
@admin.register(ShippingAddress)
class ShippingAddressAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer', 'address_line1', 'city', 'state', 'pincode')
    search_fields = ('customer__name', 'city', 'state', 'pincode')

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('order_id', 'customer', 'order_date', 'payment_status', 'order_status', 'order_amount')
    search_fields = ('order_id', 'customer__name')
    list_filter = ('payment_status', 'order_status', 'order_date')

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'order', 'product', 'quantity', 'unit_price')
    search_fields = ('order__order_id', 'product__title')
    
from .models import Vegetable, WeeklyBasket

# Register Vegetable model
@admin.register(Vegetable)
class VegetableAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)  


@admin.register(WeeklyBasket)
class WeeklyBasketAdmin(admin.ModelAdmin):
    list_display = ('id', 'get_basket_type_display', 'price')  
    search_fields = ('basket_type',)  
    list_filter = ('basket_type',)  
    
class CartAdmin(admin.ModelAdmin):
    list_display = ( 'customer','product', 'weight', 'quantity', 'product_weight_price')
    list_filter = ('product', 'weight')
    search_fields = ( 'product__title', 'weight')
    ordering = ('product',)


admin.site.register(Cart, CartAdmin)

from .models import Subscription, PaymentPlan

@admin.register(PaymentPlan)
class PaymentPlanAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'duration_days')
    search_fields = ('name',)
    
@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('user', 'payment_plan', 'is_active', 'start_date', 'end_date')
    list_filter = ('is_active', 'payment_plan')
    search_fields = ('user__username', 'payment_plan__name')
    date_hierarchy = 'start_date'
    
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ('id', 'order', 'invoice_date', 'total_amount', 'payment_status')
    list_filter = ('payment_status', 'invoice_date')
    search_fields = ('id', 'order__order_id', 'order__customer__name')
    readonly_fields = ('invoice_date', 'total_amount', 'order')

    

    def has_add_permission(self, request):
        return False

admin.site.register(Invoice, InvoiceAdmin)
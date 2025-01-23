"""
URL configuration for farmfresh project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from account import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.index,name='index'),
    path('contact/',views.contact,name='contact'),
    path('farm_tourism',views.farm_tourism,name='farm_tourism'),
    path('about/',views.about,name='about'),
    path('customer_signup/',views.customer_signup,name='customer_signup'),
   
    path('signin/',views.signin,name='signin'),
    path('signout/',views.signout,name='signout'),
    path('product/',views.product,name='product'),
    path('category/',views.category,name="category"),
    path('enquiry/',views.enquiry,name="enquiry"),
    path('add_to_cart/<int:id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/',views.cart,name='cart'),
    path('updateqty/<int:id>/',views.updateqty,name="updateqty"),
    path('product_details/<int:id>',views.product_details,name="product_details"),
    path('weekly_basket/',views.weekly_basket,name="weekly_basket"),
    path('remove_item/<int:id>/',views.remove_item,name="remove_item"),
    path('address/',views.address,name="address"),
    path('update_address/<int:id>/',views.update_address,name="update_address"),
    path('delete_address/<int:id>/',views.delete_address,name="delete_address"),
    path('confirm_order/<int:id>/',views.confirm_order,name="confirm_order"),
    path('payment/<int:id>/',views.payment,name="payment"),    
    path('payment-success/',views.payment_success,name="payment_success"),
    path('payment-plans/', views.payment_plans, name='payment_plans'),
    path('invoice/download/<int:invoice_id>/', views.download_invoice_pdf, name='download_invoice_pdf'),
    path('forgot_password/',views.forgot_password,name="forgot_password"),
    path('verify_otp/',views.verify_otp,name="verify_otp"),
    path('reset_password/<int:user_id>/',views.reset_password,name='reset_password'),
    path('track_order/',views.track_order,name='track_order'),
    path('order-details/<str:order_id>/', views.order_details, name='order_details'),
    path('profile/', views.profile, name='profile'),
    path('chatbot/', views.chatbot_view, name='chatbot'),
    
    
]
if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

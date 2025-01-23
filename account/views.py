from django.shortcuts import render,redirect
from .forms import ContactForm
from .forms import CustomerCreationForm
from django.contrib.auth.forms import AuthenticationForm
from .models import Customer
from product.models import Product,Category,OrderItem,Order,ProductWeightPrice,Cart,ShippingAddress,PaymentPlan, Subscription,Invoice
from django.contrib.auth import authenticate, login,logout
import datetime
from django.shortcuts import get_object_or_404
from datetime import timedelta
from .models import Customer, CustomUser


from django.contrib.auth.decorators import login_required
from django.utils.timezone import now



# Create your views here.

def customer_signup(request):
    if request.method=='POST':
        form = CustomerCreationForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('index')
        else:
            error='Something went wrong'
            context={'error':error}
            return render(request,'customer_signup.html',context)
    else:
        form=CustomerCreationForm()
        
    return render(request,'customer_signup.html',{'form':form})

def signin(request):
    if request.method =='POST':
        uname=request.POST['uname']
        pass1=request.POST['pass1']
        print("======================step1")
        user=authenticate(username=uname,password=pass1)
        print("======================step2",user,uname,pass1)
        if user is not None:
            login(request,user)
            print("======================step3")
            return redirect('index')
        else:
            error='Invalid Password and username'
            context={'error':error}
            return render(request,'signin.html',context)
    else:
        return render(request,'signin.html')
             
        
    
        return render(request,'signin.html')

def signout(request):
    logout(request)
    return redirect('index')



def index(request):
    return render(request,'index.html')

def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()  
            return redirect('index')  
    else:
        form = ContactForm()
    
    return render(request, 'contact_form.html', {'form': form})

def farm_tourism(request):
    return render(request,'farm_tourism.html')

def about(request):
    return render(request,'about.html')


def product(request):
    
    products = Product.objects.all()
    context ={
        'products':products
    }
    return render(request,"product.html",context)

def category(request):
    category=request.GET.get('product')
    cat_object=Category.objects.get(name=category)
    products=Product.objects.filter(category=cat_object)
    context ={
        'products':products
    }
    return render(request,"product.html",context)

def product_details(request, id):
    
    product = get_object_or_404(Product, id=id)
    
    
    weight_prices = product.weight_prices.all()
    
    
    date = datetime.datetime.today() + datetime.timedelta(hours=5)
    
    
    context = {
        'product': product,
        'weight_prices': weight_prices,
        'date': date
    }
    
    return render(request, "product_details.html", context)

def enquiry(request):
    return render(request,'enquiry.html')
 
from django.contrib import messages



def add_to_cart(request, id):
    
    product = get_object_or_404(Product, id=id)

    
    try:
        customer = Customer.objects.get(id=request.user.id)
    except Customer.DoesNotExist:
        messages.error(request, "Customer does not exist. Please sign in.")
        return redirect('signin')

    selected_weight = request.POST.get('weight')
    if not selected_weight:
        messages.error(request, "Please select a weight.")
        return redirect('product_detail', id=id)

    
    product_weight_price = get_object_or_404(ProductWeightPrice, product=product, weight=selected_weight)

    
    cart_item, created = Cart.objects.get_or_create(
        product=product,
        customer=customer,
        weight=selected_weight,
        product_weight_price=product_weight_price,
    )

    if not created:
    
        cart_item.quantity += 1
    else:
    
        cart_item.quantity = 1


    cart_item.save()

    messages.success(request, f"{product.title} ({selected_weight}) added to your cart successfully.")

    
    return redirect('cart')
def cart(request):
    if not request.user.is_authenticated:
        return redirect('signin')

    
    cart_items = Cart.objects.filter(customer__id=request.user.id)

    
    total_price = sum(item.product_weight_price.price * item.quantity for item in cart_items)

    
    context = {
        'cart_items': cart_items,
        'total_price': total_price,
    }

    return render(request, 'cart.html', context)
from .forms import WeeklyBasketForm


def weekly_basket(request):
    BASKET_PRICES = {
        'small': 500,
        'medium': 1000,
        'large': 1500,
    }

    if not request.user.is_authenticated:
        return redirect('signin')  

    subscription = Subscription.objects.filter(user=request.user, is_active=True).first()
    if not subscription:
        return redirect('payment_plans')  

    if request.method == 'POST':
        form = WeeklyBasketForm(request.POST)
        if form.is_valid():
            basket_type = form.cleaned_data['basket_type']  
            selected_vegetables = form.cleaned_data['vegetables']  
            price = BASKET_PRICES.get(basket_type, 0) 

            return render(request, 'thank_you.html', {
                'basket_type': basket_type,
                'price': price,
                'selected_vegetables': selected_vegetables,
                'subscription': subscription,
            })
    else:
        form = WeeklyBasketForm()

    return render(request, 'weekly_basket.html', {'form': form, 'subscription': subscription})

def updateqty(request, id):
    
    cart_item = Cart.objects.filter(product_id=id, customer=request.user.customer).first()

    if cart_item:
        val = request.GET.get('var')
        if val == "0":  # Decrease quantity
            if cart_item.quantity > 1:
                cart_item.quantity -= 1
        else:  
            cart_item.quantity += 1
        
        cart_item.save()
    return redirect('cart')
def remove_item(request, id):
    
    cart_items = Cart.objects.filter(product_id=id, customer=request.user.customer)
    

    if cart_items.exists():
        cart_items.delete()
    
    return redirect('cart')

def address(request):
    if request.method == 'POST':
        address_line = request.POST['address']
        landmark = request.POST['landmark']
        city = request.POST['city']
        state = request.POST['state']
        pincode = request.POST['pincode']
        user = Customer.objects.get(id=request.user.id)
        total_address = ShippingAddress.objects.filter(customer=user)
        if len(total_address) < 3:
            address = ShippingAddress.objects.create(customer=user, address_line1=address_line,landmark=landmark,city=city,state=state,pincode=pincode)
            address.save()
            return redirect('address')
        else:
            return redirect('address')


    else:
        addresses = ShippingAddress.objects.filter(customer=request.user)
        context ={
            'addresses':addresses
        }
    return render(request,'address.html',context)

def confirm_order(request, id):
    if request.user.is_authenticated:
        
        cart_items = Cart.objects.filter(customer=request.user)
        
    
        try:
            address = ShippingAddress.objects.get(id=id)
        except ShippingAddress.DoesNotExist:
        
            return redirect('address_list')  
        
        
        total_amount = 0
        for item in cart_items:
            if item.product and hasattr(item.product, 'price'):  
                total_amount += item.product.price * item.quantity
            else:
    
                total_amount += 0  
        total_price = sum(item.product_weight_price.price * item.quantity for item in cart_items)
        
        context = {
            'cart_items': cart_items,
            'address': address,
            'total_amount': total_amount,
            'total_price':total_price
        }

        return render(request, 'confirm_order.html', context)
    else:
        return redirect('signin')

def update_address(request,id):
    update_address = ShippingAddress.objects.get(id=id)
    addresses = ShippingAddress.objects.filter(customer=request.user)
    if request.method == 'POST':
        update_address.address_line1 = request.POST['address']
        update_address.landmark = request.POST['landmark']
        update_address.city = request.POST['city']
        update_address.state = request.POST['state']
        update_address.pincode = request.POST['pincode']
        update_address.save()
        return redirect('address')
        
    context ={
        'addresses':addresses,
        'update_address':update_address
        }
    return render(request,'address.html',context)
        
def delete_address(request,id):
    address = ShippingAddress.objects.get(id=id)
    address.delete()
    return redirect('address')

import random
import razorpay
def payment(request, id):
    if request.user.is_authenticated:
        
        cart_items = Cart.objects.filter(customer=request.user)
        address = get_object_or_404(ShippingAddress, id=id)

        total_amount = 0
        missing_prices = []  

        for item in cart_items:
            try:
        
                weight_price = ProductWeightPrice.objects.get(
                    product=item.product,
                    weight=item.weight 
                )
                
                total_amount += weight_price.price * item.quantity
            except ProductWeightPrice.DoesNotExist:
                
                missing_prices.append(f"Missing price for {item.product.title} with weight {item.weight}")
            
                total_amount += 0 

        
        if missing_prices:
        
            return render(request, 'error.html', {
                'message': "Some items in your cart are missing prices.",
                'missing_prices': missing_prices,
            })

        
        order_id = random.randint(1000, 9999)
        customer = get_object_or_404(Customer, id=request.user.id)
        date = datetime.date.today()

        order = Order.objects.create(
            order_id=order_id,
            customer=customer,
            order_date=date,
            shipping_address=address,
            order_amount=total_amount
        )


        for item in cart_items:
            try:
                
                weight_price = ProductWeightPrice.objects.get(
                    product=item.product,
                    weight=item.weight
                )
                OrderItem.objects.create(
                    order=order,
                    product=item.product,
                    quantity=item.quantity,
                    unit_price=weight_price.price
                )
            except ProductWeightPrice.DoesNotExist:
        
                missing_prices.append(f"Missing price for {item.product.title} with weight {item.weight}")

        
        cart_items.delete()

        
        client = razorpay.Client(auth=("rzp_test_n0lhpmrEfeIhGJ", "UOrbXQGnsEc2dhB1IFg0zNWZ"))
        data = {
            "amount": int(total_amount * 100),  
            "currency": "INR",
            "receipt": str(order_id)
        }
        payment = client.order.create(data=data)

        
        context = {
            'data': data,
            'payment': payment,
        }
        return render(request, 'pay.html', context)

    
    return render(request, 'error.html', {"message": "User is not authenticated."})


from django.contrib import messages
from django.contrib.sessions.models import Session
from django.core.mail import send_mail
from django.conf import settings
from django.urls import reverse
def payment_success(request):
    payment_id = request.GET.get('payment_id', 'N/A')
    order_id = request.GET.get('order_id', 'N/A')

    order = get_object_or_404(Order, order_id=order_id)

    order.payment_status = 'paid'
    order.save()

    invoice, created = Invoice.objects.get_or_create(
        order=order,
        defaults={
            'total_amount': order.order_amount,
            'payment_status': 'paid',
        }
    )

    download_url = reverse('download_invoice_pdf', args=[invoice.id])

    return render(request, 'payment_success.html', {
        'payment_id': payment_id,
        'order_id': order_id,
        'invoice': invoice,
        'download_url': download_url,
    })


@login_required
def payment_plans(request):
    plans = PaymentPlan.objects.all() 

    if request.method == 'POST':
        plan_id = request.POST.get('plan_id')
        plan = PaymentPlan.objects.get(id=plan_id)

        
        end_date = now() + timedelta(days=plan.duration_days)

        
        subscription, created = Subscription.objects.update_or_create(
            user=request.user,
            defaults={
                'payment_plan': plan,
                'is_active': True,
                'start_date': now(),
                'end_date': end_date,
            },
        )

        return redirect('weekly_basket')  

    return render(request, 'payment_plans.html', {'plans': plans})

from django.template.loader import render_to_string

from fpdf import FPDF

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from weasyprint import HTML



def download_invoice_pdf(request, invoice_id):
    
    invoice = get_object_or_404(Invoice, id=invoice_id)
    order = invoice.order
    print("===========================",order)
    

    order_items = OrderItem.objects.filter(order=order)
    print("===========================",order_items)
    
    
    if not order_items:
        print("No order items found for this order!")
        order_items_data = []
    else:
    
        order_items_data = []
        for item in order_items:
            total_price = item.quantity * item.unit_price  
            order_items_data.append({
                'product': item.product.title,
                'weight': item.weight,
                'quantity': item.quantity,
                'unit_price': item.unit_price,
                'total_price': total_price, 
            })

    
    formatted_date = invoice.invoice_date.strftime('%Y-%m-%d') if invoice.invoice_date else None


    context = {
        'invoice': invoice,
        'order': order,
        'order_items': order_items_data,
        'formatted_date': formatted_date,  
    }

    
    html_string = render_to_string('invoice_pdf_template.html', context)

    
    pdf_file = HTML(string=html_string).write_pdf()

    
    response = HttpResponse(pdf_file, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="invoice_{invoice.id}.pdf"'
    return response

from .forms import PasswordResetForm
from django.contrib import messages
from django.contrib.sessions.models import Session
from django.core.mail import send_mail
from django.conf import settings
def generate_otp(user):
    otp = str(random.randint(100000,999999))
    return otp
def forgot_password(request):
    if request.method == 'POST':
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            try:
                user = CustomUser.objects.get(email=email)
                otp = generate_otp(user)
                request.session['otp'] = otp
                request.session['request_user'] = user.id

                send_mail(
                    'password Reset OTP', 
                    f'Your OTP For Password Reset Is : {otp}',
                    settings.EMAIL_HOST_USER, 
                    [user.email], 
                    fail_silently=False,

                )
                return redirect('verify_otp')


            except CustomUser.DoesNotExist:
                messages.error(request,"No user found with this email")
                return render(request,'password_reset_request.html',{'form':form})
                
            


    else:
        form = PasswordResetForm()
        context = {'form': form}
    return render(request,'password_reset_request.html',{'form':form})


def verify_otp(request):
    if request.method=='POST':
        otp_entered = request.POST['otp']
        otp_stored = request.session['otp']

        if otp_entered == otp_stored:
            user_id = request.session['request_user']
            if user_id:
                user = CustomUser.objects.get(id=user_id)
                return redirect('reset_password',user_id=user.id)
            else:
                messages.error(request,"Session expired, please request OTP again.")
                return redirect('forgot_password')
        else:
            messages.error(request,"Invalid or expired OTP")
            return render(request,'verify_otp.html')



    return render(request,'verify_otp.html')
    
    
def reset_password(request, user_id):
    return render(request, 'password_reset_request.html', {'user_id': user_id})

from django.shortcuts import render, get_object_or_404

from collections import defaultdict

@login_required
def track_order(request):
    if request.method == 'POST':
        order_id = request.POST.get('order_id')

        try:
            order = Order.objects.get(order_id=order_id, customer=request.user)
            return redirect('order_details', order_id=order_id)
        except Order.DoesNotExist:
            return render(request, 'track_order.html', {'error': 'Order not found. Please check your Order ID.'})

    orders = Order.objects.filter(customer=request.user).order_by('-order_date')[:3]

    all_orders = Order.objects.filter(customer=request.user).order_by('-order_date')

    return render(request, 'track_order.html',{'orders': orders, 'all_orders': all_orders})



    
@login_required
def order_details(request, order_id):
    order = get_object_or_404(Order, order_id=order_id)

    order_items = OrderItem.objects.select_related('product').filter(order=order)

    return render(request, 'order_details.html', {'order': order, 'order_items': order_items})

from django.shortcuts import render

from django.contrib.auth.decorators import login_required

@login_required
def profile(request):
    user = request.user  
    
    try:
        customer = Customer.objects.get(id=user.id)
    except Customer.DoesNotExist:
        customer = None  
    
    orders = Order.objects.filter(customer=customer)
    
    subscription = Subscription.objects.filter(user=user).first() 
    
    context = {
        'user': user,
        'customer': customer,
        'orders': orders,
        'subscription': subscription
    }
    
    return render(request, 'profile.html', context)

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

def get_bot_response(user_message):
    user_message = user_message.lower().strip()
    responses = {
        "hello": "Howdy! I'm Farmer Bot. How can I help you today?",
        "what is farmfresh?": "FarmFresh is your one-stop shop for fresh farm produce!",
        "what products do you sell?": "We sell fresh fruits, vegetables, dairy, and more.",
        "bye": "Goodbye! Visit us again!",
        "what products do you sell?": "We offer fresh fruits, vegetables, dairy products, free-range eggs, and more!",
        "where are you located?": "We are based in the countryside, but we deliver farm-fresh produce to your doorstep.",
        "how can i place an order?": "Simply browse our website, add products to your cart, and proceed to checkout!",
        "do you deliver?": "Yes, we deliver to most areas. Let us know your location, and we can confirm the delivery availability.",
        "what are your working hours?": "Our online store is open 24/7. For support, we are available Monday to Friday, 9 AM to 6 PM.",
        "is your produce organic?": "Yes, we prioritize organic and sustainable farming practices for our produce.",
        "how do you ensure freshness?": "All our products are harvested and shipped the same day to ensure maximum freshness.",
        "can i visit the farm?": "Absolutely! We organize farm tours every weekend. Contact us to book a visit!",
        "what is organic farming?": "Organic farming is a method of agriculture that relies on natural substances and processes. It avoids synthetic fertilizers, pesticides, and genetically modified organisms (GMOs).",
    "benefits of organic farming": "Organic farming helps improve soil fertility, protects biodiversity, promotes animal welfare, and produces healthier, chemical-free food.",
    "why choose organic products?": "Organic products are free from harmful chemicals, better for your health, and environmentally friendly.",
    "how can I start organic farming?": "Starting organic farming involves using organic seeds, natural fertilizers like compost, and avoiding synthetic chemicals. Focus on soil health and pest management through natural means.",
    }
    return responses.get(user_message, "I'm not sure about that. Can you ask something else?")

@csrf_exempt
def chatbot_view(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            user_message = data.get('message', '')
            bot_response = get_bot_response(user_message)
            return JsonResponse({'response': bot_response})
        except json.JSONDecodeError:
            return JsonResponse({'response': "Invalid input."}, status=400)
    return JsonResponse({'response': "Hello, I am Farmer Bot!"})
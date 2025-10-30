from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .product import Product
from .category import Category
from django.contrib.auth.hashers import make_password
from .costomer import Customer
from django.contrib.auth.hashers import check_password
from .models import CartItem
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from django.views.decorators.csrf import ensure_csrf_cookie
from .models import CartItem

# Create your views here.
def home(request):
    categorys = Category.objects.all()
    categoryID=request.GET.get('cat')
    if categoryID:
        products = Product.get_category_id(categoryID)
    else:
        products = Product.objects.all()
    data = {
        'products': products,
        'categorys': categorys
    }
    return render(request,'index.html',data)

#signup folder
def signup(request):
    if request.method == "GET":
        return render(request,'signup.html')
    else:
        # process form data
        username = request.POST.get('username')
        email = request.POST.get('email')
        mobile = request.POST.get('mobile')
        password = request.POST.get('password')
        password = make_password(request.POST['password'])
        userdata=[username,email,mobile,password]
        print(userdata)
        uservaluse={'username':username,'email':email,'mobile':mobile,'password':password}

        #storing object
        customerdata = Customer(name=username,email=email,mobile=mobile,password=password)
        
        #vadlidation
        error_msg = None
        success_msg = None
        
        if not username:
            error_msg = "Username is required."
        elif not email:
            error_msg = "Email is required."
        elif not mobile:
            error_msg = "Mobile number is required."
        elif not password:
            error_msg = "Password is required."
        elif(Customer.objects.filter(mobile=mobile).exists()):
            error_msg = "Mobile number already exists."
        elif(Customer.objects.filter(email=email).exists()):
            error_msg = "Email already exists."
        if not error_msg:
            success_msg = "You have registered successfully."
            customerdata.save()
            msg={'success':success_msg}
            return render(request,'signup.html',msg)
        else:
            msg={'error':error_msg,'value':uservaluse}
        
            return render(request,'signup.html',msg)
        
#logo folder
def login(request):
    if request.method == "GET":
        return render(request,'login.html')
        # process form data
    email = request.POST.get('email')
    password = request.POST.get('password')
        #to check user already exists or not
    customer = Customer.get_email(email)
    if not customer:
        error_msg = "Email or Password invalid !!"
    elif not check_password(password,customer.password):
        error_msg = "Email or Password invalid !!"
    else:
        request.session['customer'] = customer.id
        return redirect ('/')
    return render(request,'login.html',{'error':error_msg,'value':{'email':email}})
#logout
from django.contrib.auth import logout as auth_logout

def logout_view(request):
    if request.method == "GET":
        auth_logout(request)  # This logs out the user by clearing session
        return render(request, 'logout.html')
    else:
        return redirect('/')
    
#cart
def cart(request):
    return render(request,'cart.html')

def add_to_cart(request):
    if request.method == "POST":
        product_id = request.POST.get('product_id')
        quantity = int(request.POST.get('quantity', 1))
        product = get_object_or_404(Product, id=product_id)
        customer_id = request.session.get('customer')

        if not customer_id:
            return redirect('login')

        cart_item, created = CartItem.objects.get_or_create(
            customer_id=customer_id,
            product=product,
            defaults={'quantity': quantity}
        )
        if not created:
            cart_item.quantity += quantity
            cart_item.save()  # Save after updating quantity
        else:
            # Quantity already set by defaults
            pass

        return redirect('cart')
    return redirect('/')


def cart_view(request):
    customer_id = request.session.get('customer')
    if not customer_id:
        return redirect('login')

    cart_items = CartItem.objects.filter(customer_id=customer_id)

    original_total = sum(item.product.price * item.quantity for item in cart_items)
    discount_total = original_total/10 # No discount info currently
    promise_fee_total = 69  # Add if you implement this field
    final_total = original_total + promise_fee_total - discount_total
    savings_total = discount_total   # Assuming savings is equal to discount

    context = {
        'cart_items': cart_items,
        'original_total': original_total,
        'discount_total': discount_total,
        'promise_fee_total': promise_fee_total,
        'final_total': final_total,
        'savings_total': savings_total,
    }
    return render(request, 'cart.html', context)

@require_POST
def update_cart(request):
    item_id = request.POST.get('item_id')
    action=request.POST.get('action')

    cart_item = get_object_or_404(CartItem, id=item_id)
    if action in ('increment', 'increase'):
        cart_item.quantity += 1
        cart_item.save()
    elif action in ('decrement', 'decrease'):
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
        else:
            cart_item.delete()
    elif action == 'remove':
        cart_item.delete() 
    return redirect('cart')

@require_POST
def place_order(request):
    customer_id = request.session.get('customer')
    if not customer_id:
        return JsonResponse({'ok':False,'error':'Please login to place order'},status=401)
    CartItem.objects.filter(customer_id=customer_id).delete()
    return JsonResponse({'ok':True})
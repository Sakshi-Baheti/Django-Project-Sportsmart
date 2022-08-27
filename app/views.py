from django.shortcuts import render, redirect
from django.views import View
from .models import Cart,Product,User,Customer,OrderPlaced
from .forms import CustomerRegistrationForm, CustomerProfileForm
from django.contrib import messages
from django.db.models import Q
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required #For function based view
from django.utils.decorators import method_decorator #For class based view


class ProductView(View):
    def get(self, request):
        topwears = Product.objects.filter(category='TW')
        bottomwears = Product.objects.filter(category='BW')
        shoes = Product.objects.filter(category='S')
        totalitem = 0
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))

        return render(request, 'app/home.html',
        {'topwears' : topwears, 'bottomwears' : bottomwears,
        'shoes' : shoes, 'totalitem' : totalitem})

class ProductDetailView(View):
    def get(self, request, pk):
        totalitem = 0
        product = Product.objects.get(pk=pk)
        item_already_in_cart = False

        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
            item_already_in_cart = Cart.objects.filter(
                Q(product=product.id) & Q(user=request.user)).exists()
        
        return render(request, 'app/productdetail.html', 
        {'product' : product, 'item_already_in_cart' : item_already_in_cart, 'totalitem' : totalitem})

@login_required
def add_to_cart(request):
    user = request.user
    product_id = request.GET.get('prod_id')
    product = Product.objects.get(id=product_id)
    cart = Cart(user=user, product=product)
    cart.save()
    return redirect('/cart')

@login_required
def show_cart(request):
    totalitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
        user = request.user
        cart = Cart.objects.filter(user=user) #cart details of currently logged in user #returns QuertSet
        amount = 0.0
        shipping_amount = 50.0
        total_amount = 0.0
        cart_product = [p for p in Cart.objects.all() if p.user == user] #Returns List
        if cart_product:
            for p in cart_product:
                temp_amount = (p.quantity * p.product.discounted_price)
                amount += temp_amount
                total_amount = amount + shipping_amount 
            return render(request, 'app/addtocart.html', {'carts' : cart,
            'total_amount' : total_amount, 'amount' : amount, 'totalitem' : totalitem})    
        else:
            return render(request, 'app/emptycart.html')

def plus_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id'] #prod_id is coming from Ajax code in myscript.js (line no 36) 
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity+=1
        c.save()
        amount = 0.0
        shipping_amount = 50.0
        cart_product = [p for p in Cart.objects.all() if p.user == request.user] #Returns List
        if cart_product:
            for p in cart_product:
                temp_amount = (p.quantity * p.product.discounted_price)
                amount += temp_amount 
            
            data = {
                'quantity' : c.quantity,
                'amount' : amount,
                'totalamount' : amount + shipping_amount
            }
            return JsonResponse(data)


def minus_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id'] #prod_id is coming from Ajax code in myscript.js (line no 36) 
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity-=1
        c.save()
        amount = 0.0
        shipping_amount = 50.0
        cart_product = [p for p in Cart.objects.all() if p.user == request.user] #Returns List
        if cart_product:
            for p in cart_product:
                temp_amount = (p.quantity * p.product.discounted_price)
                amount += temp_amount
            
            data = {
                'quantity' : c.quantity,
                'amount' : amount,
                'totalamount' : amount + shipping_amount
            }
            return JsonResponse(data)

def remove_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id'] #prod_id is coming from Ajax code in myscript.js (line no 36) 
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.delete()
        amount = 0.0
        shipping_amount = 50.0
    
        cart_product = [p for p in Cart.objects.all() if p.user == request.user] #Returns List
        if cart_product:
            for p in cart_product:
                temp_amount = (p.quantity * p.product.discounted_price)
                amount += temp_amount 
            
            data = {
                'amount' : amount,
                'totalamount' : amount + shipping_amount
            }
            return JsonResponse(data)

def buy_now(request):
 return render(request, 'app/buynow.html')

@login_required
def address(request):
    totalitem = 0
    add = Customer.objects.filter(user=request.user)
    totalitem = len(Cart.objects.filter(user=request.user))
    return render(request, 'app/address.html', {'add' : add,
    'active' : 'btn-primary', 'totalitem' : totalitem})


def shoes(request, data=None):
    if data == None:
        shoes = Product.objects.filter(category = 'S')
    elif data == 'Adidas' or data == 'Nike':
        shoes = Product.objects.filter(category = 'S').filter(brand = data)
    elif data == 'below':
        shoes = Product.objects.filter(category = 'S').filter(discounted_price__lt=10000)
    elif data == 'above':
        shoes = Product.objects.filter(category = 'S').filter(discounted_price__gt=10000)

    totalitem = 0
    totalitem = len(Cart.objects.filter(user=request.user))
    return render(request, 'app/shoes.html', {'shoes' : shoes,
    'totalitem' : totalitem})


class CustomerRegistrationView(View):
    def get(self, request):
        form = CustomerRegistrationForm()
        return render(request, 'app/customerregistration.html', {'form' : form})

    def post(self, request):
        form = CustomerRegistrationForm(request.POST)
        
        if form.is_valid():
            messages.success(request, 'Registered Successfully!!')
            form.save()
            form = CustomerRegistrationForm()
        return render(request, 'app/customerregistration.html', {'form' : form})

@login_required
def checkout(request):
    user = request.user
    address = Customer.objects.filter(user=user)
    cart_item = Cart.objects.filter(user=user)
    totalitem = 0
    amount = 0.0
    shipping_amount = 50.0
    totalamount = 0.0
    cart_product = [p for p in Cart.objects.all() if p.user == request.user] #Returns List
    if cart_product:
        for p in cart_product:
            temp_amount = (p.quantity * p.product.discounted_price)
            amount += temp_amount
        totalamount = amount +shipping_amount
    
    totalitem = len(Cart.objects.filter(user=request.user))
    return render(request, 'app/checkout.html',
    {'add' : address, 'totalamount' : totalamount,
    'cart_item' : cart_item, 'totalitem' : totalitem})

@login_required
def orders(request):
    totalitem = 0
    totalitem = len(Cart.objects.filter(user=request.user))
    order_placed = OrderPlaced.objects.filter(user=request.user)
    print(order_placed)
    return render(request, 'app/orders.html',
    {'order_placed' : order_placed, 'totalitem' : totalitem})

@login_required
def payment_done(request):
    user = request.user
    custid = request.GET.get('custid')
    customer = Customer.objects.get(id=custid)
    cart = Cart.objects.filter(user=user)
    for i in cart:
        OrderPlaced(user=user, customer=customer, product=i.product, 
        quantity = i.quantity).save()
        i.delete()
    return redirect("orders")


@method_decorator(login_required, name='dispatch')
class ProfileView(View):
    def get(self, request):
        form = CustomerProfileForm()
        totalitem = 0
        totalitem = len(Cart.objects.filter(user=request.user))
        return render(request, 'app/profile.html',
        {'form' : form, 'active' : 'btn-primary', 'totalitem' : totalitem})

    def post(self, request):
        form = CustomerProfileForm(request.POST)
        if form.is_valid():
            usr = request.user #Current user who has logged in
            name = form.cleaned_data['name']
            locality = form.cleaned_data['locality']
            city = form.cleaned_data['city']
            state = form.cleaned_data['state']
            zipcode = form.cleaned_data['zipcode']

            reg = Customer(user=usr, name=name, locality=locality, 
            city=city, state=state, zipcode=zipcode)

            reg.save()
            messages.success(request, "Congratulations! Profile Updated Successfully!")
        return render(request, 'app/profile.html', {'form' : form, 'active' : 'btn-primary'})
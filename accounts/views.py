from django.shortcuts import render, redirect
from .models import *
from .filters import OrderFilter
from django.forms import inlineformset_factory
from django.contrib.auth import authenticate, logout, login
from django.contrib.auth.decorators import login_required
from .forms import OrderForm, CustomerForm, CreateUserForm, ProductForm
from django.contrib import messages
from .decorators import unauthenticated_user, allowed_users, admin_only
from django.core.mail import send_mail
from django.conf import settings

# Create your views here.
#-----------REGISTRATION VIEWS-------------------
@unauthenticated_user
def registerPage(request):
    form = CreateUserForm()

    if request.method ==  'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')

            messages.success(request, 'Account was created for ' + username)
            return redirect('login')

    context = {'form':form}
    return render(request, 'accounts/registration/register.html', context)

@unauthenticated_user
def loginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('/')
        else:
            messages.error(request, 'Invalid Username OR Password*')

    context = {}
    return render(request, 'accounts/registration/login.html', context)

def logoutUser(request):
    logout(request)
    return redirect('login')

#-----------NEW USER CREATION VIEWS----------
@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def userPage(request):

    orders = request.user.customer.order_set.all()

    total_orders = orders.count()
    delivered = orders.filter(status='Delivered').count()
    pending = orders.filter(status='Pending').count()
    out_for_delivery = orders.filter(status='Out for delivery').count()

    context = {
        'orders': orders,
        'total_orders': total_orders,
        'delivered': delivered,
        'pending': pending,
        'out_for_delivery': out_for_delivery
        }
    return render(request, 'accounts/registration/user.html', context)

#--------------ACCOUNT SETTINGS VIEW--------------
@login_required(login_url='login')
@allowed_users(allowed_roles=['Admin','customer'])
def accountSettings(request):
    customer = request.user.customer
    form = CustomerForm(instance=customer)

    if request.method == 'POST':
        form = CustomerForm(request.POST, request.FILES, instance=customer)
        if form.is_valid():
            form.save()

            # Update User model fields explicitly
            customer.username = form.cleaned_data.get('username')
            customer.save()

    context = {'form':form}
    return render(request, 'accounts/registration/account_settings.html', context)

#-------------DASHBOARD VIEW-----------------------
@login_required(login_url='login')
@allowed_users(allowed_roles=['Admin', 'customer'])
@admin_only
def dashboard(request):
    orders = Order.objects.all().order_by('-status')[0:5]
    customers = Customer.objects.all()

    total_customers = customers.count()

    total_orders = Order.objects.all().count()
    delivered = Order.objects.filter(status='Delivered').count()
    pending = Order.objects.filter(status='Pending').count()
    out_for_delivery = Order.objects.filter(status='Out for delivery').count()

    context = {
        'customers':customers, 'orders':orders,
        'total_customers':total_customers,'total_orders':total_orders, 
        'delivered':delivered, 'pending':pending, 'out_for_delivery':out_for_delivery
	}
    return render(request, 'accounts/dashboard.html', context)

#---------------PRODUCTS VIEW------------------
@login_required(login_url='login')
@allowed_users(allowed_roles=['Admin'])
def products(request):
    products = Product.objects.all()
    context = {'products':products}
    return render(request, 'accounts/products.html', context)

#---------------CUSTOMER VIEW------------------
@login_required(login_url='login')
@allowed_users(allowed_roles=['Admin', 'customer'])
def customer(request, pk):
    customer = Customer.objects.get(id=pk)
    orders = customer.order_set.all()
    total_orders = orders.count()

    orderFilter = OrderFilter(request.GET, queryset=orders) 
    orders = orderFilter.qs

    context = {
        'customer':customer, 'orders':orders, 'total_orders':total_orders,
        'filter':orderFilter
    }
    return render(request, 'accounts/customer.html', context)

#-------------------(CREATE CUSTOMER VIEW) -------------------
@login_required(login_url='login')
@allowed_users(allowed_roles=['Admin'])
def createCustomer(request):
    action = 'create'
    form = CustomerForm()

    if request.method == 'POST':
        form = CustomerForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')

    context = {'action': action, 'form': form}
    return render(request, 'accounts/customer_form.html', context)

#-------------------(CREATE ORDER VIEW) -------------------
@login_required(login_url='login')
@allowed_users(allowed_roles=['Admin', 'customer'])
def createOrder(request, pk):
    OrderFormSet = inlineformset_factory(Customer, Order, fields=('product', 'status'), extra=3)
    customer = Customer.objects.get(id=pk)
    formset = OrderFormSet(queryset=Order.objects.none(), instance=customer)
    #action = 'create'
    #form = OrderForm(initial={'customer':customer})
    #form = OrderForm()
    if request.method == 'POST':
        formset = OrderFormSet(request.POST, instance=customer)
        # form = OrderForm(request.POST)
        if formset.is_valid():
            formset.save()
            return redirect('customer', pk=customer.id)

    total_orders = Order.objects.filter(customer=customer).count()

    context = {
        'formset': formset,
        'customer': customer,
        'total_orders': total_orders
    }
    #return render(request, 'accounts/customer.html', context)
    return render(request, 'accounts/order_form.html', context)

#-------------------(UPDATE ORDER VIEW) -------------------
@login_required(login_url='login')
#@allowed_users(allowed_roles=['Admin', 'customer'])
def updateOrder(request, pk):
	action = 'update'
	order = Order.objects.get(id=pk)
	form = OrderForm(instance=order)

	if request.method == 'POST':
		form = OrderForm(request.POST, instance=order)
		if form.is_valid():
			form.save()
			return redirect('/customer/' + str(order.customer.id))

	context =  {'action':action, 'form':form}
	return render(request, 'accounts/order_form.html', context)

#-------------------(DELETE ORDER VIEW) -------------------
@login_required(login_url='login')
#@allowed_users(allowed_roles=['Admin', 'customer'])
def deleteOrder(request, pk):
	order = Order.objects.get(id=pk)
	if request.method == 'POST':
		customer_id = order.customer.id
		customer_url = '/customer/' + str(customer_id)
		order.delete()
		return redirect(customer_url)
		
	return render(request, 'accounts/delete_item.html', {'item':order})

#--------------UPDATE CUSTOMER VIEW----------------
@login_required(login_url='login')
#@allowed_users(allowed_roles=['Admin', 'customer'])
def updateCustomer(request, pk):
    action = 'update'
    customer = Customer.objects.get(id=pk)
    form = CustomerForm(instance=customer)

    if request.method == 'POST':
        form = CustomerForm(request.POST, instance=customer)
        if form.is_valid():
            form.save()
            return redirect('/customer/' + str(customer.id))

    context = {'action': action, 'form': form}
    return render(request, 'accounts/customer_form.html', context)

#----------DELETE CUSTOMER VIEW------------------
@login_required(login_url='login')
@allowed_users(allowed_roles=['Admin'])
def deleteCustomer(request, pk):
    customer = Customer.objects.get(id=pk)
    if request.method == 'POST':
        customer.delete()
        return redirect('/')

    context = {'customer': customer}
    return render(request, 'accounts/delete_customer.html', context)

#----------CONTACT VIEW--------------
def contactSupport(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')

        # Send an email to the support team
        send_mail(
            f"Support Request from {name}",
            message,
            email,
            [settings.SUPPORT_EMAIL],  # Email where the support messages should be sent
            fail_silently=False,
        )

        messages.success(request, 'Your message has been sent! We will get back to you soon.')
        return redirect('contact')

    return render(request, 'accounts/contact.html')

#-------Product pages views------
def order_management(request):
    return render(request, 'accounts/products/order_management.html')

def customer_insights(request):
    return render(request, 'accounts/products/customer_insights.html')

def support_portal(request):
    return render(request, 'accounts/products/support_portal.html')

def about(request):
    return render(request, 'accounts/products/about.html')

# def privacy(request):
#     return render(request, 'accounts/products/privacy.html')

def help_center(request):
    return render(request, 'accounts/products/help_center.html')
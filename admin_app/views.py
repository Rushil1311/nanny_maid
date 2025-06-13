from django.shortcuts import render,HttpResponse,redirect
from razorpay import Payment
from admin_app import forms 
from admin_app import models
from nm_app.models import ServiceResponse, Subscription, User , Service_form
from django.contrib.auth import login,logout,authenticate
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import  login_required , user_passes_test 
from .models import SubscriptionPlan, NannySubscription
from datetime import datetime, timedelta, timezone


from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.contrib import messages
from nm_app.models import feedback

# Create your views here.
@login_required
def homeview(request):
    return render(request,'adminapp/home.html')

# def hello(request):
#     return HttpResponse("this is demo app")


@login_required(login_url='user_login')
def adminindexview(request):
    return render(request,'adminapp/index.html')


@login_required(login_url='user_login')
def forms_editors(request):
    if request.method == "POST":
        form = forms.editorsForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(List_services)
        else:
            print("error")
            print(form.errors)
    return render(request,'adminapp/forms-editors.html')


@login_required(login_url='user_login')
def add_services(request):
    if request.method == "POST":
        form = forms.Service(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.user = request.user
            obj.save()
            return redirect(List_services)
        else:
            print("error")
            print(form.errors)
    return render(request,'adminapp/add-services.html')


@login_required(login_url='user_login')
def List_services(request):
    data = models.Service.objects.all()
    context = {'data':data}
    return render(request,'adminapp/List-service.html',context=context)

@login_required(login_url='user_login')
def service_update(request,id):
    data = models.Service.objects.get(id=id)
    if request.method == "POST":
        form = forms.Service(request.POST,instance=data)
        if form.is_valid():
            form.save()
            return redirect(List_services)
        else:
            print("error")
            print(form.errors)
    context = {'data':data}
    return render(request,'adminapp/update-service.html',context=context)

@login_required(login_url='user_login')
def service_delete(request,id):
    data = models.Service.objects.get(id=id)
    data.delete()
    return redirect(List_services)

@login_required(login_url='user_login')
def add_category(request):
    if request.method == "POST":
        form = forms.Category_form(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            return redirect(List_category)
        else:
            print("error")
            print(form.errors)
    return render(request,'adminapp/add-category.html')

@login_required(login_url='user_login')
def List_category(request):
    data = models.Category.objects.all()
    context = {'data':data}
    return render(request,'adminapp/List_category.html',context=context)

@login_required(login_url='user_login')
def category_delete(request,id):
    data = models.Category.objects.get(id=id)
    data.delete()
    return redirect(List_category)

# @login_required
# def category_update(request,id):
#     data = models.Category.objects.get(id=id)
#     if request.method == "POST":
#         form = forms.Category_form(request.POST,instance=data)
#         if form.is_valid():
#             form.save()
#             return redirect(List_category)
#         else:
#             print("error")
#             print(form.errors)
#     context = {'data':data}
#     return render(request,'adminapp/category-update.html',context=context)


@login_required(login_url='user_login')
def category_update(request, id):
    data = models.Category.objects.get(id=id)
    if request.method == "POST":
        form = forms.Category_form(request.POST, request.FILES, instance=data)  # <- Notice request.FILES
        if form.is_valid():
            form.save()
            return redirect(List_category)
        else:
            print("error")
            print(form.errors)
    else:   
        form = forms.Category_form(instance=data)
    
    context = {'form': form}
    return render(request, 'adminapp/category-update.html', context=context)

def pages_registration(request):
    if request.method == "POST":
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')
        password1 = request.POST.get('password1', '')

        if not all([username, password, password1]):
            return HttpResponse("All fields are required.")

        try:
            validate_email(username)
        except ValidationError:
            return HttpResponse("Invalid email format.")

        if password != password1:
            return HttpResponse("Passwords do not match.")

        if User.objects.filter(username=username).exists():
            return HttpResponse("Username already exists.")

        User.objects.create_user(
            username=username,
            password=password,
            is_superuser=True,
            is_staff=True,
            role="admin"
        )
        return redirect(pages_login)

    return render(request, 'adminapp/pages-register.html')


def pages_login(request):
    if request.method =="POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username,password=password)
        if user is not None:
            login(request,user)
            return redirect(adminindexview)
        else:
            return HttpResponse("User does not exist")
    return render(request,'userapp/register.html')

def logoutview(request):
    logout(request)
    return redirect(pages_login)

@login_required(login_url='user_login')
def pages_contact(request):
    return render(request,'adminapp/pages-contact.html')

@login_required(login_url='user_login')
def my_profile(request):
    user = request.user
    return render(request, 'adminapp/admin-profile.html', {'data': user})

@login_required
def my_profile(request):
    return render(request, 'adminapp/admin-profile.html', {'user': request.user})


@login_required
def edit_admin_profile(request):
    user = request.user

    if request.method == 'POST':
        user.first_name = request.POST.get('first_name')
        user.last_name = request.POST.get('last_name')
        user.email = request.POST.get('email')
        user.phone = request.POST.get('phone')
        user.address = request.POST.get('address')

        if 'profile' in request.FILES:
            user.profile = request.FILES['profile']

        user.save()
        messages.success(request, 'Profile updated successfully!')
        return redirect('admin-profile')

    return render(request, 'adminapp/edit-admin-profile.html')

# def category_add(request):
#     return render(request,'adminapp/')
 


@login_required(login_url='user_login')
def Service_Requests(request):
   data = Service_form.objects.all()
   context = {'data':data}
   return render(request,'adminapp/service_requests.html',context=context)



# def request_delete(request,id):
#     data = Service_form.objects.get(id=id)
#     data.delete()
#     return redirect(Service_Requests)



@login_required(login_url='user_login')
def manage_nanny(request):
    nanny = models.User.objects.filter(role="maid",is_active=True)
    context = {
        'nanny':nanny,
    }
    return render(request,'adminapp/manage-nanny.html',context)

@login_required(login_url='user_login')
def manage_booking(request):
    return render(request,'adminapp/manage-booking.html')



def manage_subscriptions(request):
    plans = SubscriptionPlan.objects.all()
    return render(request, "adminapp/manage-subscription.html", {"plans": plans})

def update_subscription_price(request, plan_id):
    plan = get_object_or_404(SubscriptionPlan, id=plan_id)
    new_price = request.POST.get("price")
    if new_price:
        plan.price = new_price
        plan.save()
    return redirect("manage_subscriptions")

@login_required(login_url='user_login')
def view_feedback(request):
    feedback_list = feedback.objects.all().order_by('-id')  # or '-created_at' if added
    context = {'data': feedback_list}
    return render(request, 'adminapp/view-feedback.html', context)

@login_required(login_url='user_login')
def manage_payment(request):
    return render(request,'adminapp/manage-payment.html')




@login_required(login_url='user_login')
def subscription_page(request):
    plans = SubscriptionPlan.objects.all()
    return render(request, "subscriptions.html", {"plans": plans})

@login_required(login_url='user_login')
def subscribe(request, plan_id):
    plan = get_object_or_404(SubscriptionPlan, id=plan_id)
    nanny = request.user

    # Check if the nanny already has an active subscription
    existing_subscription = NannySubscription.objects.filter(nanny=nanny, is_active=True).first()
    if existing_subscription:
        existing_subscription.is_active = False
        existing_subscription.save()

    # Create a new subscription
    new_subscription = NannySubscription.objects.create(
        nanny=nanny, plan=plan, start_date=datetime.now(), end_date=datetime.now() + timedelta(days=plan.duration_days)
    )
    return redirect("subscription_success")

@login_required(login_url='user_login')
def nanny_requests(request):
     data = models.User.objects.filter(role="maid")
     context = {'data':data}
     return render(request,'adminapp/nanny_requests.html',context=context)

@login_required(login_url='user_login')
def nanny_acceptview(request,id):
    nanny = models.User.objects.get(id=id)
    nanny.is_active=True
    nanny.save()
    return redirect(nanny_requests)

@login_required(login_url='user_login')
def nanny_rejectview(request,id):
    nanny = models.User.objects.get(id=id)
    nanny.is_active=False
    nanny.save()
    return redirect(nanny_requests)

@login_required(login_url='user_login')
def Nanny_delete_Request(request,id):
    data = models.User.objects.get(id=id)
    data.delete()
    return redirect(nanny_requests)



def service_payments(request):
    data = ServiceResponse.objects.select_related('maid', 'service', 'service__user').all().order_by('-id')

    context = {
        "data": data
    }
    return render(request, "adminapp/service_payments.html", context)



def subscription_list(request):
    subscriptions = Subscription.objects.select_related('user', 'payment').all()
    return render(request, 'adminapp/subscription_list.html', {'subscriptions': subscriptions})


def admin_subscription_details(request, user_id):
    # Get the user
    user = User.objects.get(id=user_id)
    
    # Get the user's subscription and payment history
    subscription = Subscription.objects.filter(user=user).first()  # Assuming one active subscription at a time
    payments = Payment.objects.filter(user=user)
    
    context = {
        'user': user,
        'subscription': subscription,
        'payments': payments,
    }
    
    return render(request, 'admin_subscription_details.html', context)

from django.db.models import Q

def admin_subscription_list(request):
    search_query = request.GET.get('search', '')
    status_filter = request.GET.get('status', '')
    today = timezone.now().date()

    # Base queryset
    subscriptions = Subscription.objects.select_related('user', 'plan')

    # Filter by username or email
    if search_query:
        subscriptions = subscriptions.filter(
            Q(user__username__icontains=search_query) |
            Q(user__email__icontains=search_query)
        )

    # Filter by status
    if status_filter == "active":
        subscriptions = subscriptions.filter(end_date__gte=today)
    elif status_filter == "expired":
        subscriptions = subscriptions.filter(end_date__lt=today)

    return render(request, "admin_app/subscription_list.html", {
        "subscriptions": subscriptions,
        "today": today,
    })

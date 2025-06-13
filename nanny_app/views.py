import json
from pyexpat.errors import messages
from django.shortcuts import get_object_or_404, render,redirect
from razorpay import Payment
from admin_app.models import SubscriptionPlan
from nm_app import forms 
from nm_app import models
from django.http import HttpResponse, JsonResponse
from django.contrib.auth import logout,authenticate,login as auth_login
from nm_app import views
from admin_app.views import adminindexview
from django.contrib.auth.decorators import login_required
from admin_app.views import adminindexview
# Create your views here.

@login_required(login_url='user_login')
def nannyindexview(request):
    return render(request,'nanny_maidapp/index.html')


def nanny_register(request):
     if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        address = request.POST.get('address')
        phone = request.POST.get('phone')
        password = request.POST.get('password')
        password1 = request.POST.get('password1')
        if password == password1:
            try:
                models.User.objects.get(username=email)
                return HttpResponse("Email already exists")
            except:
                models.User.objects.create_user(username=email,
                                                first_name=name,
                                                email=email,
                                                address=address,
                                                phone=phone,
                                                password=password,
                                                )
                return redirect(nanny_register)
        else:
            return HttpResponse("Password does not match")
     return render(request,'nanny_maidapp/register.html')



def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)

        if user is not None:
            if models.User.role == "Maid" and models.User.is_staff: 
                if models.User.is_active:  # Ensures only approved chefs can log in
                    auth_login(request, models.User)
                    return redirect(nannyindexview)
                else:
                    messages.error(request, "Your account is not yet approved by the admin. Please wait for approval.")
            elif models.User.role == "admin" and models.User.is_superuser:
                auth_login(request, models.User)
                return redirect(adminindexview)
            elif models.User.role == "Customer":
                auth_login(request, models.User)
                return redirect(views.userindexview)
        else:
            messages.error(request, "Invalid username or password. Please try again.")
    return render(request,'userapp/index.html')

def ulogoutview(request):
    logout(request)
    return redirect('user_login')

def nanny_contact(request):
    return render(request,'nanny_maidapp/nuser-contact.html')


def nabout_us(request):
    return render(request,'nanny_maidapp/about-us.html')

@login_required(login_url='user_login')
def nanny_profile(request):
    data = models.User.objects.get(username=request.user.username)
    context = {'data':data}
    return render(request,'nanny_maidapp/user_profile.html',context)


def our_services(request):
    return render(request,'nanny_maidapp/our-services.html')

@login_required(login_url='user_login')
def team_list(request):

    return render(request,'nanny_maidapp/team-list.html')

@login_required(login_url='user_login')
def manage_maid(request):
    maid = models.User.objects.filter(role=models.User.MAID)
    return render(request, 'adminapp/manage-profile.html', {'maid': maid})


@login_required(login_url='user_login')
def accept_maid(request, owner_id):
    owner = get_object_or_404(models.User, id=owner_id)

    if not owner.is_verify:
        owner.is_verify = True  # Approve owner
        owner.is_active = True  # Allow login
        owner.save()

        messages.success(request, 'Furniture owner has been approved.')

        # Send email notification to the owner
        subject = "Your Account Has Been Approved - Furniture Rental"
        message = f"""
        Dear {owner.username},

        Congratulations! Your account on  nanny maid app has been approved.
        You can now log in and start managing your services listings.

        Best Regards,
        nanny/maid Team
        """
        send_mail(subject, message, 'your_email@gmail.com', [owner.email]) # type: ignore

    else:
        owner.is_verify = False  # Revoke authorization
        owner.is_active = False  # Disable login
        owner.save()

        messages.warning(request, 'Furniture owner authorization has been revoked.')

    return redirect('manage_owners')

@login_required(login_url='user_login')
def delete_maid(request, owner_id):     
    owner = get_object_or_404(models.User, id=owner_id, role=models.User.MAID)
    owner.delete()
    messages.success(request, 'Furniture owner deleted successfully.')
    return redirect('manage_owners')

# def jobtype_add():
# def jobtype_list():
# def jobtype_update():
# def jobtype_delete():

# def profile(request):
#     return redirect(profile_page) 

@login_required(login_url='user_login')
def dashboard(request):
    service = models.Service_form.objects.filter(status='Pending')
    if request.method == "POST":
        service_id = request.POST.get('service')
        service_data = models.Service_form.objects.get(id=service_id)
        base_price = request.POST.get('base_price')
        description = request.POST.get('description')
        # print("service",service_data)
        print("base_price",base_price)
        print("description",description)
        response = models.ServiceResponse.objects.create(maid=request.user,
                                                         service=service_data,
                                                         description=description,
                                                         base_price=base_price,
                                                         )
        print("response",response)
        return redirect(dashboard)
    
    
    context = {
        'service':service,
    }
    return render(request, "nanny_maidapp/dashboard.html",context)

@login_required(login_url='user_login')
def accept_order(request, request_id):
    """ Nanny/Maid accepts a service request """
    service_request = get_object_or_404(models.ServiceRequest, id=request_id)

    # Update the request to mark it as accepted
    service_request.nanny_or_maid = request.user
    service_request.is_accepted = True
    service_request.save()

    return redirect("dashboard")

@login_required(login_url='user_login')
def view_accepted_orders(request):
    return render(request,'nanny_maidapp/view-accepted-orders.html')

@login_required(login_url='user_login')
def view_requests(request):
    data = models.ServiceResponse.objects.filter(maid=request.user,status="Approved")
    print("dattta",data)
    context = {'data':data}
    return render(request,'nanny_maidapp/view-requests.html',context=context)



# def subscription(request):
#     return render(request,'nanny_maidapp/subscription.html')

def subscription(request):
    default_plans = [
        {'name': 'monthly', 'price': 299, 'duration_days': 30},
        {'name': 'quarterly', 'price': 799, 'duration_days': 90},
        {'name': 'yearly', 'price': 2499, 'duration_days': 365},
    ]

    # Create missing default plans
    for plan_data in default_plans:
        SubscriptionPlan.objects.get_or_create(
            name=plan_data['name'],
            defaults={
                'price': plan_data['price'],
                'duration_days': plan_data['duration_days']
            }
        )

    plans = SubscriptionPlan.objects.all()  # or Subscription.objects.all()
    return render(request, 'nanny_maidapp/subscription.html', {'plans': plans})


@login_required(login_url='user_login')
def n_edit_profile(request):
    if request.method == "POST":
        user = request.user
        user.first_name = request.POST['first_name']
        user.last_name = request.POST['last_name']
        user.email = request.POST['email']
        user.save()
        return redirect('nanny_profile')  # Redirect to profile page

    return render(request, "nanny_maidapp/n_edit_profile.html")



def subscription_details(request):
    user = request.user
    if not user.is_authenticated:
        return JsonResponse({"error": "Unauthorized"}, status=403)

    # Fetch the most recent active or expired subscription for the user
    subscription = Subscription.objects.filter(user=user).order_by('-created_at').first()

    if not subscription:
        return JsonResponse({"error": "No subscription found."}, status=404)

    # Return subscription details in a response (JSON or render a template)
    subscription_data = {
        "plan_name": subscription.plan_name,
        "status": subscription.status,
        "start_date": subscription.start_date,
        "end_date": subscription.end_date,
        "amount": subscription.amount,
        "is_active": subscription.is_active,
    }

    return JsonResponse({"subscription": subscription_data})

def subscription_details(request):
    user = request.user
    if not user.is_authenticated:
        return render(request, 'error.html', {"message": "Unauthorized"})

    # Fetch the most recent active or expired subscription for the user
    subscription = Subscription.objects.filter(user=user).order_by('-created_at').first()

    if not subscription:
        return render(request, 'error.html', {"message": "No subscription found."})

    # Pass the subscription data to the template
    context = {
        'subscription': subscription
    }

    return render(request, 'subscription_details.html', context)


# ----------------------------------------------------------------------------------------------------------------------------------
import razorpay
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import os
from nm_app .models import Payment, Subscription
# Load Razorpay credentials
RAZORPAY_KEY_ID = os.getenv('RAZORPAY_KEY_ID')
RAZORPAY_KEY_SECRET = os.getenv('RAZORPAY_KEY_SECRET')

razorpay_client = razorpay.Client(auth=(RAZORPAY_KEY_ID, RAZORPAY_KEY_SECRET))

@csrf_exempt
def create_order(request):
    if request.method == "POST":
        user = request.user
        plan_name = request.POST.get("plan_name")
        amount = int(request.POST.get("amount")) * 100

        order_data = {
            "amount": amount,
            "currency": "INR",
            "payment_capture": 1,
        }
        order = razorpay_client.order.create(order_data)

        # Save payment info
        Payment.objects.create(
            user=user,
            plan_name=plan_name,
            amount=amount / 100,
            razorpay_order_id=order["id"],
            status="Created"
        )

        return JsonResponse({
            "id": order["id"],
            "amount": order["amount"],
            "currency": order["currency"],
            "razorpay_key": RAZORPAY_KEY_ID  # send key to frontend
        })



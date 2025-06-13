from datetime import timedelta
import json
import os
from pyexpat.errors import messages
from django.shortcuts import get_object_or_404, render,redirect
from dotenv import load_dotenv
from nm_app import forms 
from nm_app import models
from django.http import HttpResponse
from django.contrib.auth import login,logout,authenticate, login as auth_login
from django.contrib import messages
from admin_app.models import Category, Service, SubscriptionPlan
from django.contrib.auth.decorators import login_required
from nanny_app.views import nannyindexview
from admin_app.views import adminindexview

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from django.conf import settings


from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.contrib import messages

from django.core.mail import send_mail
from django.utils.timezone import now
from django.contrib.auth.hashers import make_password
import random
from .models import OTP, Payment, Subscription, User
from django.contrib.auth import update_session_auth_hash
import razorpay


from django.contrib.sessions.backends.db import SessionStore
# views.py


# Create your views here.

def userindexview(request):
    maid = models.User.objects.filter(role="maid", is_active=True)
    context = {
        "maid": maid,
    }
    return render(request,'userapp/index.html',context) 

# Password strength checker
def is_strong_password(password):
    if len(password) < 8:
        return "Password must be at least 8 characters long."
    if not re.search(r"[A-Z]", password):
        return "Password must include at least one uppercase letter."
    if not re.search(r"[a-z]", password):
        return "Password must include at least one lowercase letter."
    if not re.search(r"\d", password):
        return "Password must include at least one digit."
    if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        return "Password must include at least one special character."
    return None



def user_register(request):
    context = {}
    if request.method == "POST":
        name = request.POST.get('name', '').strip()
        email = request.POST.get('email', '').strip()
        address = request.POST.get('address', '').strip()
        phone = request.POST.get('phone', '').strip()
        password = request.POST.get('password', '')
        password1 = request.POST.get('password1', '')
        profile = request.FILES.get('profile')

        errors = {}

        if not all([name, email, address, phone, password, password1]):
            errors['form'] = "All fields are required."

        try:
            validate_email(email)
        except ValidationError:
            errors['email'] = "Invalid email format."

        if not phone.isdigit() or len(phone) < 10:
            errors['phone'] = "Phone number must be at least 10 digits."

        if password != password1:
            errors['password'] = "Passwords do not match."
        else:
            password_validation = is_strong_password(password)
            if password_validation:
                errors['password'] = password_validation

        if User.objects.filter(username=email).exists():
            errors['email_exists'] = "Email already exists."

        if errors:
            context['errors'] = errors
            context['values'] = request.POST
            return render(request,'userapp/register.html', context)

        user = User.objects.create_user(
            username=email,
            first_name=name,
            email=email,
            address=address,
            phone=phone,
            role='customer',
            password=password,
            profile=profile,
        )
        return redirect('user_login')
    
    return redirect('user_login')


# def user_register(request):
#     if request.method == "POST":
#         name = request.POST.get('name', '').strip()
#         email = request.POST.get('email', '').strip()
#         address = request.POST.get('address', '').strip()
#         phone = request.POST.get('phone', '').strip()
#         phone = request.POST.get('phone', '').strip()
#         profile = request.POST.get('profile', '').strip()
#         password = request.POST.get('password', '')
#         password1 = request.POST.get('password1', '')

#         if not all([name, email, address, phone, password, password1]):
#             return HttpResponse("All fields are required.")

#         try:
#             validate_email(email)
#         except ValidationError:
#             return HttpResponse("Invalid email format.")

#         if not phone.isdigit() or len(phone) < 10:
#             return HttpResponse("Phone number must be at least 10 digits.")

#         if password != password1:
#             return HttpResponse("Passwords do not match.")

#         if User.objects.filter(username=email).exists():
#             return HttpResponse("Email already exists.")

#         User.objects.create_user(
#             username=email,
#             first_name=name,
#             email=email,
#             address=address,
#             role="customer",
#             phone=phone,
#             profile=profile,
#             password=password,
            
#         )
        
#         return redirect(user_register)

#     return render(request, 'userapp/register.html')

# --------------------------------------------------------------------------------------------------------------------------------------------
import re
# Generate OTP Function
def generate_otp():
    return str(random.randint(100000, 999999))  # Generates a 6-digit OTP

# ✅ Normal Login Function (Without OTP)
def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)

        if user is not None:
            if user.is_active:
                auth_login(request, user)  # ✅ Directly log in the user
                messages.success(request, "Login successful!")

                # Redirect based on user role
                if user.role == "maid" and user.is_staff:
                    return redirect('nannyindexview')
                elif user.role == "admin" and user.is_superuser:
                    return redirect('adminindexview')
                elif user.role == "customer":
                    return redirect('userindexview')
            else:
                messages.error(request, "Your account is not yet approved by the admin.")
        else:
            messages.error(request, "Invalid username or password. Please try again.")

    return render(request, 'userapp/register.html')  # ✅ Changed to login.html

# ✅ Forgot Password View (Sends OTP)
def forgot_password(request):
    if request.method == 'POST':
        email = request.POST['email']
        user = User.objects.filter(email=email).first()

        if user:
            send_otp_email(user)  # ✅ Send OTP via email
            request.session['reset_email'] = email  # Store email in session
            return redirect('verify_otp')  # Redirect to OTP verification page
        else:
            messages.error(request, "No account found with this email.")
    
    return render(request, 'userapp/forgot_password.html')  # ✅ Fixed template path

# ✅ Send OTP Function
def send_otp_email(user):
    otp = generate_otp()  # Generate OTP
    OTP.objects.create(user=user, otp_code=otp)  # Save OTP in the database

    subject = "Your OTP for Password Reset"
    message = f"Hello {user.username},\n\nYour OTP for resetting your password is: {otp}\n\nThis OTP is valid for 5 minutes."
    from_email = settings.EMAIL_HOST_USER  # ✅ Uses settings email
    send_mail(subject, message, from_email, [user.email])

# ✅ OTP Verification View (For Forgot Password Only)
def verify_otp(request):
    if request.method == 'POST':
        entered_otp = request.POST.get('otp')
        email = request.session.get('reset_email')  # Retrieve email from session
        user = User.objects.filter(email=email).first()

        if user:
            otp_obj = OTP.objects.filter(user=user).order_by('-created_at').first()
            if otp_obj and otp_obj.is_valid() and otp_obj.otp_code == entered_otp:
                request.session['otp_verified'] = True  # ✅ Mark OTP as verified
                return redirect('reset_password')  # Redirect to reset password page
            else:
                messages.error(request, "Invalid or expired OTP.")
    
    return render(request, 'userapp/verify_otp.html')  # ✅ OTP input page



# ✅ Password Reset View (Only After OTP Verification)

def reset_password(request):
    if not request.session.get('otp_verified'):
        return redirect('forgot_password')  # Ensure OTP is verified before resetting password

    if request.method == 'POST':
        password1 = request.POST['new_password1']
        password2 = request.POST['new_password2']

        if password1 == password2:
            email = request.session.get('reset_email')
            user = User.objects.filter(email=email).first()

            if user:
                user.password = make_password(password1)  # Hash and save the new password
                user.save()

                # Clear session data
                request.session.pop('otp_verified', None)
                request.session.pop('reset_email', None)

                messages.success(request, "Password reset successful. You can now log in.")
                return redirect('user_login')  # Redirect to login page
            else:
                messages.error(request, "User not found. Please try again.")
        else:
            messages.error(request, "Passwords do not match.")

    return render(request, 'userapp/password_reset.html')  # Render password reset form




def user_logout(request):
    logout(request)
    return render(request, 'userapp/register.html', {'form_type': 'login'})


def user_contact(request):
    return render(request,'userapp/user-contact.html')

def about_us(request):
    return render(request,'userapp/about-us.html')

@login_required(login_url='user_login')
def user_profile(request):
    data = models.User.objects.get(username=request.user.username)
    context = {'data':data}
    return render(request,'userapp/user_profile.html',context)

def our_services(request):
    data = Category.objects.all()
    context = {'data':data}
    return render(request,'userapp/our-services.html',context)


@login_required(login_url='user_login')
def service_request_form(request):
    services = Service.objects.all()  # fetch services from DB

    if request.method == "POST":
        form = forms.service_request_form(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.user = request.user
            obj.save()
            return redirect('userindexview')  # make sure this is the correct named URL
        else:
            print("error")
            print(form.errors)
    else:
        form = forms.service_request_form()

    return render(request, 'userapp/service_form.html', {
        'form': form,
        'services': services
    })


# def service_request_form(request):
#     if request.method == "POST":
#         form = forms.service_request_form(request.POST)
#         if form.is_valid():
#             obj = form.save(commit=False)
#             obj.user = request.user
#             obj.save()
#             return redirect(service_request_form)
#         else:
#             print("error")
#             print(form.errors)
#     return render(request,'userapp/service_form.html')

def pricing(request):
    return render(request,'userapp/pricing.html')

# def team_member(request):
#     if request.method == "POST":
#         name = request.POST.get('name', '').strip()
#         email = request.POST.get('email', '').strip()
#         address = request.POST.get('address', '').strip()
#         profile = request.POST.get('profile', '').strip()
#         phone = request.POST.get('phone', '').strip()
#         password = request.POST.get('password', '')
#         password1 = request.POST.get('password1', '')

#         # Basic validation
#         if not all([name, email, address, phone, password, password1]):
#             return HttpResponse("All fields are required.")

#         try:
#             validate_email(email)
#         except ValidationError:
#             return HttpResponse("Invalid email format.")

#         if not phone.isdigit() or len(phone) < 10:
#             return HttpResponse("Phone number must be at least 10 digits.")

#         if password != password1:
#             return HttpResponse("Passwords do not match.")

#         if User.objects.filter(username=email).exists():
#             return HttpResponse("Email already exists.")

#         User.objects.create_user(
#             username=email,
#             first_name=name,
#             email=email,
#             address=address,
#             phone=phone,
#             password=password,
#             is_active=False,
#             is_staff=True,
#             role="maid"
#         )
#         return redirect(userindexview)

#     return render(request, 'userapp/team-member.html')



def team_member(request):
    if request.method == "POST":
        name = request.POST.get('name', '').strip()
        email = request.POST.get('email', '').strip()
        address = request.POST.get('address', '').strip()
        phone = request.POST.get('phone', '').strip()
        experience = request.POST.get('experience', '').strip()
        speciality = request.POST.get('speciality', '').strip()
        password = request.POST.get('password', '')
        password1 = request.POST.get('password1', '')

        profile = request.FILES.get('profile')
        adhar_pan = request.FILES.get('adhar_pan')

        # Check for missing fields
        if not all([name, email, address, phone, experience, speciality, password, password1, profile, adhar_pan]):
            return HttpResponse("All fields are required.")

        # Validate email
        try:
            validate_email(email)
        except ValidationError:
            return HttpResponse("Invalid email format.")

        # Validate phone number
        if not phone.isdigit() or len(phone) < 10:
            return HttpResponse("Phone number must be at least 10 digits.")

        # Validate experience
        if not experience.isdigit() or int(experience) < 0:
            return HttpResponse("Experience must be a valid non-negative number.")

        # Password match
        if password != password1:
            return HttpResponse("Passwords do not match.")

        # Password strength
        if len(password) < 8 or not re.search(r'[A-Z]', password) or \
           not re.search(r'[a-z]', password) or not re.search(r'\d', password) or \
           not re.search(r'[\W_]', password):
            return HttpResponse("Password must be at least 8 characters long and contain uppercase, lowercase, number, and special character.")

        # Check if user exists
        if User.objects.filter(username=email).exists():
            return HttpResponse("Email already exists.")

        # Create user
        user = User.objects.create_user(
            username=email,
            first_name=name,
            email=email,
            password=password,
            address=address,
            phone=phone,
            profile=profile,
            verification_doc=adhar_pan,  # Assuming you have a field like this
            role="maid",
            is_active=False,
            is_staff=True,
            speciality=speciality,
            experience=int(experience)
        )

        return redirect('userindexview')  # Change to actual route name

    return render(request, 'userapp/team-member.html')

def team_list(request):
    return render(request,'userapp/team-list.html')

def List_category(request):
    data = Category.objects.filter(user=request.user)
    context = {'data':data}
    return render(request,'adminapp/List_category.html',context=context)

@login_required(login_url='user_login')
def feedback(request):
    if request.method == "POST":
        form = forms.feedback(request.POST)
        if form.is_valid():
            form.save()
            return redirect(userindexview)
        else:
            print("error")
            print(form.errors)
    return render(request,'userapp/feedback.html')

    
@login_required(login_url='user_login')
def my_orders(request):
    return render(request,'userapp/my-order.html')

@login_required(login_url='user_login')
def completed_orders(request):
    return render(request,'userapp/completed-orders.html')


@login_required(login_url='user_login')
def my_requests(request):
    data = models.Service_form.objects.filter(user=request.user)
    context = {
        'data':data,
    }
    return render(request,'userapp/my_requests.html',context)


@login_required(login_url='user_login')
def request_details(request, id):
    """ View to display service request details """
    service = get_object_or_404(models.Service_form, id=id)
    data = models.ServiceResponse.objects.filter(service=service)

    # Set payment status
    for item in data:
        # Update status only if not already paid
        if item.payment_status == "Pending" and item.status == "Approved":
            item.payment_status = "Pending"
        elif item.payment_status == "Pending" and item.status == "Paid":
            item.payment_status = "Paid"
        
        item.save()

    context = {
        "data": data,
        "service": service,
        "razorpay_key_id": settings.RAZORPAY_KEY_ID  # ✅ Add this line
    }
    return render(request, "userapp/request_details.html", context)



@login_required
def create_razorpay_order(request, id):
    # Ensure the method is POST
    if request.method == "POST":
        data = json.loads(request.body)  # Parse the incoming JSON body
        amount = data.get("amount", 0)  # Get amount from JSON data
        
        if amount <= 0:
            return JsonResponse({"error": "Invalid amount"}, status=400)

        client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
        
        # Create order
        order = client.order.create(dict(
            amount=amount,
            currency="INR",
            payment_capture=1
        ))

        # Return the order details as a JSON response
        return JsonResponse({'order_id': order['id'], 'amount': order['amount']})
    else:
        return JsonResponse({"error": "Invalid request method"}, status=405)
@csrf_exempt
def service_payment_success(request):
    import json
    from .models import Payment, ServiceResponse

    data = json.loads(request.body)

    # Create payment record
    Payment.objects.create(
        user=request.user,
        plan_name="Nanny Service",
        amount=float(data.get("amount", 0)) / 100,
        razorpay_order_id=data['razorpay_order_id'],
        razorpay_payment_id=data['razorpay_payment_id'],
        razorpay_signature=data['razorpay_signature'],
        status="Completed"
    )

    # Update ServiceResponse status
    try:
        service = ServiceResponse.objects.get(id=data['service_id'])

        # Prevent payment status update if it's already 'Paid'
        if service.payment_status == "Pending":
            service.payment_status = "Paid"
            service.status = "Completed"  # Set the status to completed after payment
            service.save()

    except ServiceResponse.DoesNotExist:
        return JsonResponse({"error": "Service not found"}, status=404)

    return JsonResponse({"status": "success"})


def request_accept_view(request, id):
    """ View to approve a service request """
    service_response = get_object_or_404(models.ServiceResponse, id=id)
    service_response.status = "Approved"
    service_response.save()
    
    messages.success(request, "Service request Approved successfully.")
    return redirect("request_details", id=service_response.service.id)



def request_reject_view(request, id):
    """ View to reject a service request """
    service_response = get_object_or_404(models.ServiceResponse, id=id)
    service_response.status = "Rejected"
    service_response.save()
    
    messages.error(request, "Service request rejected.")
    return redirect("request_details", id=service_response.service.id)


def p1(request):
    return render(request,'userapp/p1.html')

@login_required(login_url='user_login')
def edit_profile(request):
    if request.method == "POST":
        user = request.user
        user.first_name = request.POST['first_name']
        user.last_name = request.POST['last_name']
        user.email = request.POST['email']
        
        # Safely access the uploaded file
        profile_pic = request.FILES.get('profile')
        if profile_pic:
            user.profile = profile_pic  # assuming user.profile is an ImageField
        user.save()
        return redirect('user_profile')  # Redirect to profile page

    return render(request, "userapp/edit_profile.html")

import razorpay

# ----------------------------------------------------------------------------------------------------------------------------------
import razorpay
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import os
from .models import Payment

# Load Razorpay credentials
RAZORPAY_KEY_ID = os.getenv('RAZORPAY_KEY_ID')
RAZORPAY_KEY_SECRET = os.getenv('RAZORPAY_KEY_SECRET')

razorpay_client = razorpay.Client(auth=(RAZORPAY_KEY_ID, RAZORPAY_KEY_SECRET))

# @csrf_exempt
# def create_order(request):
#     if request.method == "POST":
#         user = request.user
#         plan_name = request.POST.get("plan_name")
#         amount = int(request.POST.get("amount")) * 100

#         order_data = {
#             "amount": amount,
#             "currency": "INR",
#             "payment_capture": 1,
#         }
#         order = razorpay_client.order.create(order_data)

#         # Save payment info
#         Payment.objects.create(
#             user=user,
#             plan_name=plan_name,
#             amount=amount / 100,
#             razorpay_order_id=order["id"],
#             status="Created"
#         )

#         return JsonResponse({
#             "id": order["id"],
#             "amount": order["amount"],
#             "currency": order["currency"],
#             "razorpay_key": RAZORPAY_KEY_ID  # send key to frontend
#         })


import logging
logger = logging.getLogger(__name__)

@csrf_exempt
def create_order(request):
    # Add detailed logging for all requests
    logger.info(f"Request method: {request.method}")
    logger.info(f"Content type: {request.content_type}")

    plan_name = None  # Initialize plan_name and amount_str
    amount_str = None

    if request.method == "POST":
        # Log POST data for debugging
        logger.info(f"POST data: {dict(request.POST)}")

        user = request.user

        # Check if the request body might contain JSON
        if request.content_type == 'application/json':
            try:
                body_data = json.loads(request.body)
                logger.info(f"JSON body: {body_data}")
                # Extract values from JSON
                plan_name = body_data.get("plan_name")
                amount_str = body_data.get("amount")
            except json.JSONDecodeError:
                logger.error("Invalid JSON in request body")
                return JsonResponse({"error": "Invalid JSON data", "razorpay_key": RAZORPAY_KEY_ID}, status=400)
        else:
            # Extract values from form data
            plan_name = request.POST.get("plan_name")
            amount_str = request.POST.get("amount")

        # Log extracted values
        logger.info(f"User: {user}, Plan: {plan_name}, Amount: {amount_str}")

        # Check authentication
        if not request.user.is_authenticated:
            logger.warning("Unauthenticated user attempted to create order")
            return JsonResponse({"error": "Authentication required", "razorpay_key": RAZORPAY_KEY_ID}, status=401)

        # Validate plan_name and amount_str
        if not plan_name or not amount_str:
            logger.warning("Empty plan_name or amount_str submitted")
            return JsonResponse({"error": "Plan name and amount are required", "razorpay_key": RAZORPAY_KEY_ID}, status=400)

        try:
            amount = int(amount_str)  # already in paise
            logger.info(f"Processed amount: {amount}")
        except ValueError:
            logger.error(f"Invalid amount value: {amount_str}")
            return JsonResponse({"error": "Invalid amount format", "razorpay_key": RAZORPAY_KEY_ID}, status=400)

        try:
            # Prepare order data
            order_data = {
                "amount": amount,
                "currency": "INR",
                "payment_capture": 1,
            }
            logger.info(f"Creating Razorpay order with data: {order_data}")

            # Create order via Razorpay API
            order = razorpay_client.order.create(order_data)
            logger.info(f"Razorpay order created: {order['id']}")

            # Save payment info in database
            payment = Payment.objects.create(
                user=user,
                plan_name=plan_name,
                amount=amount / 100,
                razorpay_order_id=order["id"],
                status="Created"
            )
            logger.info(f"Payment record created: {payment.id}")

            # Return success response
            return JsonResponse({
                "id": order["id"],
                "amount": order["amount"],
                "currency": order["currency"],
                "razorpay_key": RAZORPAY_KEY_ID
            })
        except Exception as e:
            logger.exception(f"Error processing payment: {str(e)}")
            return JsonResponse({
                "error": f"Payment processing error: {str(e)}",
                "razorpay_key": RAZORPAY_KEY_ID
            }, status=500)

    # If not POST method
    logger.warning(f"Invalid request method: {request.method}")
    return JsonResponse({
        "error": "Only POST method is allowed",
        "razorpay_key": RAZORPAY_KEY_ID
    }, status=405)

@login_required(login_url='user_login')
def payments(request):
    return render(request, "userapp/payments.html", {"razorpay_key": RAZORPAY_KEY_ID})

from django.views.decorators.http import require_POST
from django.utils import timezone



@csrf_exempt
@require_POST
def payment_success(request):
    user = request.user
    if not user.is_authenticated:
        return JsonResponse({"error": "Unauthorized"}, status=403)

    # Check if the user already has an active subscription
    active_subscription = Subscription.objects.filter(user=user, is_active=True).first()

    if active_subscription:
        # If the subscription has not expired, prevent purchase
        if active_subscription.end_date > timezone.now():
            return JsonResponse({"error": "You already have an active subscription. Wait until it expires to purchase a new one."}, status=400)
    
    razorpay_order_id = request.POST.get("razorpay_order_id")
    razorpay_payment_id = request.POST.get("razorpay_payment_id")
    razorpay_signature = request.POST.get("razorpay_signature")

    try:
        # Get the corresponding payment object
        payment = Payment.objects.get(razorpay_order_id=razorpay_order_id, user=user)
        payment.razorpay_payment_id = razorpay_payment_id
        payment.razorpay_signature = razorpay_signature
        payment.status = "Success"
        payment.save()

        # Parse duration from the plan name
        plan_name = payment.plan_name.lower()
        today = timezone.now()

        if "3 month" in plan_name:
            end_date = today + timezone.timedelta(days=90)
        elif "6 month" in plan_name:
            end_date = today + timezone.timedelta(days=180)
        elif "1 year" in plan_name or "12 month" in plan_name:
            end_date = today + timezone.timedelta(days=365)
        else:
            end_date = today + timezone.timedelta(days=30)  # default fallback

        # Optional: deactivate old subscriptions
        Subscription.objects.filter(user=user, is_active=True).update(is_active=False)

        # Create new subscription
        Subscription.objects.create(
            user=user,
            plan_name=payment.plan_name,
            amount=payment.amount,
            payment=payment,
            status="Active",
            start_date=today,
            end_date=end_date,
            is_active=True
        )

        return JsonResponse({"message": "Payment successful. Subscription activated!"})

    except Payment.DoesNotExist:
        return JsonResponse({"error": "Payment not found"}, status=404)

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




from django.contrib.auth.views import (
    PasswordResetView,
    PasswordResetDoneView,
    PasswordResetConfirmView,
    PasswordResetCompleteView
)
from django.urls import path, reverse_lazy

class CustomPasswordResetView(PasswordResetView):
    template_name = 'userapp/password_reset_form.html'
    email_template_name = 'userapp/password_reset_email.html'
    subject_template_name = 'userapp/password_reset_subject.txt'
    success_url = reverse_lazy('password_reset_done')

class CustomPasswordResetDoneView(PasswordResetDoneView):
    template_name = 'userapp/password_reset_done.html'

class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'userapp/password_reset_confirm.html'
    success_url = reverse_lazy('password_reset_complete')

    def form_valid(self, form):
        print("✅ Password reset successful! Redirecting...")
        form.save()
        return redirect(self.success_url) 

class CustomPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = 'userapp/password_reset_complete.html'

urlpatterns = [
    path("password/reset/done/", CustomPasswordResetDoneView.as_view(), name="password_reset_done"),
]



@login_required(login_url='user_login')
def nanny_reviews(request):
    reviews = feedback.objects.filter(nanny=request.user)  # Fetch reviews for the logged-in nanny
    return render(request, 'userapp/nanny_reviews.html', {'reviews': reviews})
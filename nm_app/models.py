from datetime import timedelta
from arrow import now
from django.db import models
from django.contrib.auth.models import AbstractUser,User
# Create your models here.


class User(AbstractUser):
    
    phone = models.IntegerField(null=True,blank=True)
    address = models.TextField(null=True,blank=True)
    role = models.CharField(max_length=255,null=True,blank=True,default="customer")
    profile =models.ImageField(null=True,blank=True)
    skills = models.TextField(null=True,blank=True)
    adhar_pan = models.ImageField(null=True,blank=True)
    certificate = models.ImageField(null=True,blank=True)
    is_verify = models.BooleanField(default=False)
    speciality = models.CharField(max_length=255,null=True,blank=True)
    expirience = models.IntegerField(null=True,blank=True)
    

class nanny_maid(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    address = models.TextField()
    phone = models.IntegerField()
    year =models.CharField(max_length=20)
    profile =models.ImageField()
    rating =models.IntegerField()

class services(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField()
    address = models.TextField()
    phone = models.IntegerField()
    # desc = models.TextField()
    # price =models.IntegerField()
    # duration = models.DateTimeField()
    # availability =models.BooleanField()




class job_type(models.Model):
    name = models.CharField(max_length=50)
    desc = models.TextField(null=True,blank=True)

class service_event(models.Model):
    name = models.CharField(max_length=50)
    desc = models.TextField()
    nanny_maid =models.ForeignKey(nanny_maid,on_delete=models.CASCADE)

# class feedback(models.Model):
    
#     nanny_maid =models.ForeignKey(nanny_maid,on_delete=models.CASCADE)
#     user = models.ForeignKey(User,on_delete=models.CASCADE)
#     rating =models.IntegerField()
#     comment =models.TextField()
#     created_at =models.DateTimeField()

class maid_request(models.Model):
    service_event =models.ForeignKey(service_event,on_delete=models.CASCADE)

class booking(models.Model):
    service_event =models.ForeignKey(service_event,on_delete=models.CASCADE)

class Service_form(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    date = models.DateField() 
    time = models.TimeField()
    service_type = models.CharField(max_length=50) 
    address = models.CharField(max_length=100)
    Description = models.CharField(max_length=50)
    location = models.CharField(max_length=200,null=True,blank=True)
    status = models.CharField(max_length=255,null=True,blank=True,default='Pending')
    is_paid = models.BooleanField(default=False)
    payment = models.CharField(max_length=255,null=True,blank=True)


# class ServiceResponse(models.Model):
#     service = models.ForeignKey(Service_form,on_delete=models.CASCADE,related_name='service_response')
#     maid = models.ForeignKey(User,on_delete=models.CASCADE)
#     base_price = models.IntegerField()
#     description = models.TextField(null=True,blank=True)
#     is_send = models.BooleanField(default=True)
#     status = models.CharField(
#         max_length=255, 
#         choices=[("Pending", "Pending"), ("Approved", "Approved"), ("Rejected", "Rejected")], 
#         default="Pending"
#     )

class ServiceResponse(models.Model):
    service = models.ForeignKey(Service_form, on_delete=models.CASCADE, related_name='service_response')
    maid = models.ForeignKey(User, on_delete=models.CASCADE)
    base_price = models.IntegerField()
    description = models.TextField(null=True, blank=True)
    is_send = models.BooleanField(default=True)
    status = models.CharField(
        max_length=255, 
        choices=[("Pending", "Pending"), ("Approved", "Approved"), ("Rejected", "Rejected")], 
        default="Pending"
    )
    payment_status = models.CharField(
        max_length=20,
        choices=[("Pending", "Pending"), ("Paid", "Paid")],
        default="Pending"
    )


class ServiceRequest(models.Model):
    REQUEST_TYPE_CHOICES = [
        ('general', 'General Request'),
        ('personal', 'Personal Request'),
    ]   

    customer_name = models.CharField(max_length=100)
    nanny_or_maid = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    request_type = models.CharField(max_length=10, choices=REQUEST_TYPE_CHOICES)
    details = models.TextField()
    is_accepted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.customer_name} - {self.request_type} ({'Accepted' if self.is_accepted else 'Pending'})"
    
class feedback(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField()
    feedback = models.TextField()


class OTP(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    otp_code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)

    def is_valid(self):
        expiration_time = self.created_at + timedelta(minutes=5)  # OTP valid for 5 minutes
        return now() <= expiration_time



class Payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Store who made the payment
    plan_name = models.CharField(max_length=50)  # Subscription plan name
    amount = models.DecimalField(max_digits=10, decimal_places=2)  # Amount paid
    razorpay_order_id = models.CharField(max_length=100, unique=True)  # Razorpay Order ID
    razorpay_payment_id = models.CharField(max_length=100, blank=True, null=True)  # Razorpay Payment ID
    razorpay_signature = models.CharField(max_length=255, blank=True, null=True)  # Signature for verification
    status = models.CharField(max_length=20, default="Pending")  # Payment Status
    created_at = models.DateTimeField(auto_now_add=True)  # Timestamp

    def __str__(self):
        return f"{self.user.username} - {self.plan_name} - {self.status}"
    


class Subscription(models.Model):
    PLAN_CHOICES = [
        ('3_months', '3 Months Subscription'),
        ('6_months', '6 Months Subscription'),
        ('1_year', '1 Year Subscription'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    plan_name = models.CharField(max_length=20, choices=PLAN_CHOICES)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment = models.ForeignKey(Payment, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, default="Active")
    created_at = models.DateTimeField(auto_now_add=True)

    # 🆕 Add these:
    start_date = models.DateTimeField(null=True, blank=True)
    end_date = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username} - {self.plan_name} - {self.status}"

    @property
    def get_price_in_paise(self):
        return int(self.amount * 100)
    

class NannyReview(models.Model):
    nanny = models.ForeignKey(User, on_delete=models.CASCADE, related_name="nanny_reviews")
    reviewer = models.ForeignKey(User, on_delete=models.CASCADE, related_name="given_reviews")  # Parent or employer
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)])  # Rating from 1 to 5
    comment = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review for {self.nanny.username} by {self.reviewer.username}"
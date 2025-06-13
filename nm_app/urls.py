from django.contrib import admin
from django.urls import path,include
from nm_app import views
from django.contrib.auth import get_user_model
CustomUser = get_user_model()
from .models import OTP  # Import only if you have the OTP model


urlpatterns = [
   path('',views.userindexview,name='userindexview'),

   path('user_register/',views.user_register,name="user_register"),

   path('user_login/',views.user_login,name="user_login"),
   
   path('about_us/',views.about_us,name="about_us"),
   
   path('our_services/',views.our_services,name="our_services"),
   
   path('pricing/',views.pricing,name="pricing"),

   # path('Service_form/',views.Service_form,name="Service_form"),
    
   path('user_profile/',views.user_profile,name="user_profile"),

   path('user_contact/',views.user_contact,name="user_contact"),

   path('team_member/',views.team_member,name="team_member"),

   path('team_list/',views.team_list,name="team_list"),

   path('service_request_form/',views.service_request_form,name="service_request_form"),

   path('feedback/',views.feedback,name="feedback"),

   path('create-order/', views.create_order, name='create_order'),

   path('my_orders/', views.my_orders, name='my_orders'),

#    path('ulogoutview/', views.ulogoutview, name='ulogoutview'),
     path('user_logout/', views.user_logout, name='user_logout'),

   path('completed_orders/', views.completed_orders, name='completed_orders'),
   path('my_requests/', views.my_requests, name='my_requests'),
   path('p1/', views.p1, name='p1'),
   path('edit-profile/', views.edit_profile, name='edit-profile'),

    path('create-order/<int:id>/', views.create_razorpay_order, name='create_razorpay_order'),
    path('service/payment/success/', views.service_payment_success, name='service_payment_success'),


   # path("request-details/<int:id>/", views.request_details, name="request_details"),

    path("service/details/<int:id>/", views.request_details, name="request_details"),
    path("request_accept_view/<int:id>/", views.request_accept_view, name="request_accept_view"),
    path("request_reject_view/<int:id>/", views.request_reject_view, name="request_reject_view"),


    path('forgot-password/', views.forgot_password, name='forgot_password'),
    path('verify-otp/', views.verify_otp, name='verify_otp'),
    path('reset-password/', views.reset_password, name='reset_password'),
   
   
    path('verify-otp/', views.verify_otp, name='verify-otp'),

    path("payments/", views.payments, name="payments"),
    path("payment_success/", views.payment_success, name="payment_success"),

    path('password/reset/', views.CustomPasswordResetView.as_view(), name='password_reset'),
    path('password/reset/done/', views.CustomPasswordResetDoneView.as_view(), name='password_reset_done'),
    path('password/reset/<uidb64>/<token>/', views.CustomPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('password/reset/complete/', views.CustomPasswordResetCompleteView.as_view(), name='password_reset_complete'),

    path('nanny/reviews/', views.nanny_reviews, name='nanny_reviews'),
   
]



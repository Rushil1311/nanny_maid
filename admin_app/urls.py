from django.contrib import admin
from django.urls import path,include
from admin_app import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('homeview/',views.homeview,name="homeview"),

    # path('hello/',views.hello,name="hello"),

    path('adminindexview/',views.adminindexview,name="adminindexview"),

    path('add_services/',views.add_services,name="add_services"),

    path('forms_editors/',views.forms_editors,name="forms_editors"),
    
    path('add_category/',views.add_category,name="add_category"),

    path('List_services/',views.List_services,name="List_services"),

    path('service_delete/<int:id>/',views.service_delete,name="service_delete"),

    path('service_update/<int:id>/',views.service_update,name="service_update"),

    path('List_category/',views.List_category,name="List_category"),

    path('category_delete/<int:id>/',views.category_delete,name="category_delete"),

    path('category_update/<int:id>/',views.category_update,name="category_update"),

    path('pages_login/',views.pages_login,name="pages_login"),
    
    path('logoutview/',views.logoutview,name="logoutview"),

    path('pages_registration/',views.pages_registration,name="pages_registration"),

    path('pages_contact/',views.pages_contact,name="pages_contact"),

    path('my_profile/',views.my_profile,name="my_profile"),    

    path('Service_Requests/',views.Service_Requests,name="Service_Requests"),

    path('manage_nanny/',views.manage_nanny,name="manage_nanny"),

    path('manage_booking/',views.manage_booking,name="manage_booking"),

    path('manage_subscriptions/',views.manage_subscriptions,name="manage_subscriptions"),

    path('subscription-plans/update/<int:plan_id>/', views.update_subscription_price, name='update_subscription_price'),

    path('view_feedback/',views.view_feedback,name="view_feedback"),

    path('manage_payment/',views.manage_payment,name="manage_payment"),

    path('nanny_requests/',views.nanny_requests,name="nanny_requests"),

    path('edit_admin_profile/', views.edit_admin_profile, name='edit_admin_profile'),

    path('nanny_acceptview/<int:id>/',views.nanny_acceptview,name="nanny_acceptview"),
    path('nanny_rejectview/<int:id>/',views.nanny_rejectview,name="nanny_rejectview"),

    # path('request_delete/',views.request_delete,name="request_delete"),  
    path('Nanny_delete_Request/',views.Nanny_delete_Request,name="Nanny_delete_Request"),  
    path('admin/subscriptions', views.subscription_list, name='subscription_list'),

    path('subscription/<int:user_id>/', views.admin_subscription_details, name='admin_subscription_details'),

    path('admin/service-payments/', views.service_payments, name='service_payments'),


]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)    


from django.contrib import admin
from django.urls import path,include
from nanny_app import views

urlpatterns = [
   path('nannyindexview/',views.nannyindexview,name='nannyindexview'),

   path('nanny_register/',views.nanny_register,name="nanny_register"),

#    path('nanny_login/',views.nanny_login,name="nanny_login"),
   
   path('nabout_us/',views.nabout_us,name="nabout_us"),
    
   path('nanny_profile/',views.nanny_profile,name="nanny_profile"),

   path('nanny_contact/',views.nanny_contact,name="nanny_contact"),
   path('subscription/',views.subscription,name="subscription"),


#    path('team_member/',views.team_member,name="team_member"),

   path('team_list/',views.team_list,name="team_list"),

    path('ulogoutview/',views.ulogoutview,name="ulogoutview"),
    
    path('manage-maid/', views.manage_maid, name='manage_maid'),
    path('accept-maid/<int:owner_id>/', views.accept_maid, name='accept_maid'),
    path('delete-maid/<int:owner_id>/', views.delete_maid, name='delete_maid'),

    path("dashboard/", views.dashboard, name="dashboard"),
    path("view_requests/", views.view_requests, name="view_requests"),
    path("view_accepted_orders/", views.view_accepted_orders, name="view_accepted_orders"),
    path("n_edit_profile/", views.n_edit_profile, name="n_edit_profile"),

    path('subscription-details/', views.subscription_details, name='subscription_details'),

]

from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.dashboard, name='home'),
    #-------REGISTRATION VIEWS-----------
    path('register/', views.registerPage, name='register'),
    path('login/', views.loginPage, name='login'),
    path('logout/', views.logoutUser, name='logout'),
    path('user/', views.userPage, name='user'),
    path('contact/', views.contactSupport, name='contact'),

    #---ACCOUNT SETTINGS URL----------
    path('account/', views.accountSettings, name='account'),

    path('products/', views.products, name='products'),
    path('customer/<str:pk>/', views.customer, name='customer'),

    #------------ (CREATE URLS) ------------
    path('create_customer/', views.createCustomer, name='create_customer'),
    #path('create_order/', views.createOrder, name='create_order'),
    path('create_order/<str:pk>/', views.createOrder, name='create_order'),

    #------------ (UPDATE URLS) ----------------------
    path('update_order/<str:pk>/', views.updateOrder, name="update_order"),
    path('customer/update/<str:pk>/', views.updateCustomer, name='update_customer'),


    #------------ (DELETE URLS) -----------------------
    path('delete_order/<str:pk>/', views.deleteOrder, name="delete_order"),
    path('customer/delete/<str:pk>/', views.deleteCustomer, name='delete_customer'),

    #------------PASSWORD RESET URLS--------------
    path(
        'reset_password/', auth_views.PasswordResetView.as_view(template_name='accounts/registration/password_reset.html'), 
        name='reset_password'), # Submit email form
    path(
        'reset_password_sent/', auth_views.PasswordResetDoneView.as_view(template_name='accounts/registration/password_reset_done.html'), 
        name='password_reset_done'), # Email sent success message
    path(
        'reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='accounts/registration/password_reset_confirm.html'), 
        name='password_reset_confirm'), # Link to Password reset form in email
    path(
        'reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(template_name='accounts/registration/password_reset_complete.html'), 
        name='password_reset_complete'), # password successfully changed message
    
    # Product Pages
    path('order-management/', views.order_management, name='order_management'),
    path('customer-insights/', views.customer_insights, name='customer_insights'),
    path('support-portal/', views.support_portal, name='support_portal'),

    path('about/', views.about, name='about'),
    # path('privacy/', views.privacy, name='privacy'),
    path('help_center/', views.help_center, name='help_center'),
]

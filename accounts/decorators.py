from django.http import HttpResponse
from django.shortcuts import render, redirect

def unauthenticated_user(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('/')
        else:
            return view_func(request, *args, **kwargs)
    return wrapper_func

def allowed_users(allowed_roles=[]):
    def decorator(view_func):
        def wrapper_func(request, *args, **kwargs):
            group = None
            if request.user.groups.exists():
                group = request.user.groups.all()[0].name

            if group in allowed_roles:
                return view_func(request, *args, **kwargs)
            else:
                # Render a custom error page with a message and options for navigation
                context = {
                    'message': 'You do not have the necessary permissions to access this page. Please contact an administrator if you believe this is a mistake.'
                }
                return render(request, 'accounts/permission_denied.html', context)
                
        return wrapper_func
    return decorator

def admin_only(view_func):
    def wrapper_function(request, *args, **kwargs):
        group = None
        if request.user.groups.exists():
            group = request.user.groups.all()[0].name

        if group == 'customer':
            return redirect('user')  # Redirect to the user page if the group is 'customer'
        
        if group == 'Admin':
            return view_func(request, *args, **kwargs)  # Call the view if the group is 'Admin'
        
        # Render a custom error page for unauthorized access
        context = {
            'message': 'You are not authorized to view this admin page. Please log in with an admin account.'
        }
        return render(request, 'accounts/permission_denied.html', context)

    return wrapper_function


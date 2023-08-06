===================================
django-user-login-register-activate
===================================

django-user-login-register-activate is a django app to make user login and registration


Quick start
-----------
1. To install from PyPi::

	pip install django-user-login-register-activate
	
2. Add "login" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...
        'login',
    ]
3. Include the login URLconf in your project urls.py like this::

	from django.contrib import admin
	from django.urls import path, include

	urlpatterns = [
		...
		path('accounts/', include('login.urls')),
	]
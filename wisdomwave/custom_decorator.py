from django.shortcuts import render,redirect,HttpResponseRedirect
from functools import wraps
from django.contrib.auth.decorators import login_required, user_passes_test


def user_is_admin_or_superuser(user):
    return user.is_authenticated and (user.role == 'admin' or user.is_superuser)


def admin_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if request.user.is_admin() or request.user.is_superuser:
            return view_func(request, *args, **kwargs)
        else:
            return HttpResponseRedirect("Permission Denied")
    return _wrapped_view

def only_teacher_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if request.user.is_teacher():
            return view_func(request, *args, **kwargs)
        else:
            return HttpResponseRedirect("Permission Denied")
    return _wrapped_view
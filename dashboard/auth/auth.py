import random

from django.contrib.auth import login, logout, authenticate
from django.shortcuts import render, redirect

# Create your views here.
from dashboard.models.user import User

rdbg = ['blue', 'azure', 'green', 'purple']


def sign_in(requests):
    if not requests.user.is_anonymous:
        return redirect('home')

    ctx = {
        "rdbg": rdbg[random.randint(0, len(rdbg) - 1)]
    }
    if requests.POST:
        username = requests.POST.get('phone')
        password = requests.POST.get('pass')

        user = User.objects.filter(phone=username).first()
        if not user:
            ctx["error"] = True
            return render(requests, 'auth/login.html', ctx)

        if not user.check_password(password):
            ctx["error"] = True
            return render(requests, 'auth/login.html', ctx)

        if not user.is_superuser or not user.is_staff:
            ctx["staff_error"] = True
            return render(requests, 'auth/login.html', ctx)

        login(requests, user)

        return redirect('home')

    return render(requests, 'auth/login.html', ctx)


def sign_up(requests):
    ctx = {
        "rdbg": rdbg[random.randint(0, len(rdbg) - 1)]
    }
    return render(requests, 'auth/regis.html', ctx)


def sign_out(requests, conf=False):
    if requests.user.is_anonymous:
        return redirect("sign-in")

    if not conf:
        return render(requests, "auth/conf_out.html")

    logout(requests)

    return redirect("sign-in")


def otp(requests):
    if not requests.session.get('token'):
        return redirect('sign-in')

    return render(requests, 'otp.html')


def index(requests):
    if requests.user.is_anonymous:
        return redirect("sign-in")

    ctx = {
        "home": True,
    }

    return render(requests, 'dashboard/base.html', ctx)

import random
import uuid

from django.contrib.auth import login, logout, authenticate
from django.shortcuts import render, redirect

# Create your views here.
from base.helper import generate_key, code_hashing, check_otp
from dashboard.models.extra import Otp
from user.models import User

rdbg = ['blue', 'azure', 'green', 'purple']


def sign_in(requests):
    if not requests.user.is_anonymous:
        return redirect('home')

    ctx = {
        "rdbg": rdbg[random.randint(0, len(rdbg) - 1)]
    }
    if requests.POST:
        phone = requests.POST.get('phone')
        password = requests.POST.get('pass')

        user = User.objects.filter(phone=phone).first()
        if not user:
            ctx["error"] = True
            return render(requests, 'auth/login.html', ctx)

        if not user.check_password(password):
            ctx["error"] = True
            return render(requests, 'auth/login.html', ctx)

        otp = random.randint(100000, 999999)
        code = generate_key(50) + "$" + str(otp) + "$" + uuid.uuid4().__str__()
        hashed = code_hashing(code)
        requests.session['otp'] = otp

        root = Otp.objects.create(
            key=hashed,
            mobile=phone,
            extra={},
            step="sms-send",
            by=2
        )
        root.save()
        requests.session['token'] = hashed
        requests.session['st'] = 'otp'
        return redirect('otp')

    return render(requests, 'auth/login.html', ctx)


def sign_up(requests):
    if not requests.user.is_anonymous:
        return redirect('home')
    ctx = {
        "rdbg": rdbg[random.randint(0, len(rdbg) - 1)]
    }
    try:
        del requests.session['token']
    except:
        pass
    try:
        del requests.session['otp']
    except:
        pass
    if requests.POST:
        phone = requests.POST.get('phone')
        password = requests.POST.get('pass')
        re_password = requests.POST.get('re_pass')

        user = User.objects.filter(phone=phone).first()
        if user:
            ctx["user_error"] = True
            return render(requests, 'auth/regis.html', ctx)

        if password != re_password:
            ctx["re_error"] = True
            return render(requests, 'auth/regis.html', ctx)

        otp = random.randint(100000, 999999)
        code = generate_key(50) + "$" + str(otp) + "$" + uuid.uuid4().__str__()
        hashed = code_hashing(code)
        requests.session['otp'] = otp

        Otp.objects.create(
            key=hashed,
            mobile=phone,
            extra={},
            step="sms-send",
            by=1
        )
        requests.session['token'] = hashed
        requests.session['password'] = password
        requests.session['st'] = 'otp'
        return redirect('otp')

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

    if requests.session['st'] == 'otp' and requests.POST:
        code = requests.POST.get('otp')
        otp = Otp.objects.filter(key=requests.session['token']).first()
        ctx = check_otp(otp, code)
        if 'status' not in ctx:
            return render(requests, 'auth/otp.html', ctx)

        if otp.by == 2:
            user = User.objects.get(phone=otp.mobile)
            login(requests, user)
            del requests.session['token']
            del requests.session['st']
            return redirect('home')

        if otp.by == 1:
            user = User.objects.create_user(
                phone=otp.mobile,
                password=requests.session['password']
            )
            authenticate(requests)
            login(requests, user)
            del requests.session['token']
            del requests.session['st']
            del requests.session['password']
            return redirect('home')

    requests.session['st'] = 'otp'
    return render(requests, 'auth/otp.html')


def index(requests):
    if requests.user.is_anonymous:
        return redirect("sign-in")

    ctx = {
        "home": True,
    }

    return render(requests, 'dashboard/base.html', ctx)

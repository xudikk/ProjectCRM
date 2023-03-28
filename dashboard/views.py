import random

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

# Create your views here.
from dashboard.forms import EnrollForm
from dashboard.models.extra import Member, GroupStudent
from dashboard.student.forms import StudentForm


@login_required(login_url='sign-in')
def index(request):
    mb = Member.objects.filter(user=request.user).first()
    ctx = {}
    if not mb:
        return redirect('student-new')
    ctx['member'] = mb
    request.session['user'] = mb.id
    if not mb.position:
        ctx.update({
            "ekey": "np"  # error key - need position
        })
        return render(request, 'base.html', ctx)

    if mb.permission == 3:
        return redirect('admin-home')

    group = GroupStudent.objects.filter(student=mb).first()
    if not group:
        ctx.update({
            "ekey": "ng"  # error key - need group
        })
        return render(request, 'base.html', ctx)

    return render(request, 'base.html', ctx)


@login_required(login_url='sign-in')
def new(requests):
    ctx = {}
    try:
        ins = Member.objects.get(user=requests.user)
        ctx['member'] = ins
    except:
        ins = None

    form = StudentForm(requests.POST or None, requests.FILES or None, instance=ins)
    if form.is_valid():
        form.instance.user = requests.user
        form.instance.phone_number = requests.user.phone
        form.save()

        requests.user.firstname = requests.POST.get("firstname", '')
        requests.user.lastname = requests.POST.get("lastname", '')
        requests.user.nickname = requests.POST.get("nickname", '')
        requests.user.save()
        return redirect("home")
    else:
        print(form.errors)

    ctx.update({
        "form": form,
    })
    return render(requests, "student/self_create.html", ctx)


@login_required(login_url='sign-in')
def st_profile(requests):
    member = Member.objects.raw(f"""
        select dm.* from dashboard_member dm
        where dm.user_id={requests.user.id} 
    """)

    ctx = {
        "member": member[0]
    }
    return render(requests, 'profile.html', ctx)


def enroll(requests):
    form = EnrollForm(requests.POST or None)
    if form.is_valid():
        form.save()
        ctx = {
            "added": True,
            'ekey': 'enroll',
            "form": form
        }
        return render(requests, "base.html", ctx)

    ctx = {
        'ekey': 'enroll',
        "form": form
    }

    return render(requests, "base.html", ctx)

from django.shortcuts import render, redirect

from dashboard.models.extra import Member
from dashboard.student.forms import StudentForm


def new(requests):
    if requests.user.is_anonymous:
        return redirect('sign-in')
    try:
        ins = Member.objects.get(user=requests.user)
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

    ctx = {
        "form": form,
        "section": 'student'
    }
    return render(requests, "student/self_create.html", ctx)


def st_index(requests):
    if requests.user.is_anonymous:
        return redirect('sign-in')

    return render(requests, 'student/index.html', {})


def st_profile(requests):
    member = Member.objects.raw(f"""
        select uu.*, dm.* from dashboard_member dm
        inner join user_user uu on uu.id=dm.user_id
        where dm.user_id={requests.user.id} 
    """)

    for i in member:
        print(i)

    ctx = {
        "member": member[0]
    }
    return render(requests, 'student/profile.html', ctx)
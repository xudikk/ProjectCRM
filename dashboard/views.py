import random

from django.shortcuts import render, redirect


# Create your views here.
from dashboard.models.extra import Member


def index(request):
    if request.user.is_anonymous:
        return redirect("sign-in")
    mb = Member.objects.filter(user=request.user).first()
    if not mb:
        return redirect('student-new')

    if not mb.position:
        ctx = {
            "ekey": "np"  # error key - need position
        }
        return render(request, 'base.html', ctx)

    # if mb.is_student:
    #     return redirect("student-index")
    ctx = {}

    return render(request, 'base.html', ctx)




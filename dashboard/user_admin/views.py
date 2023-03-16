from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from dashboard.models.extra import Member, Group, Interested
from dashboard.user_admin.forms import MemberChangeForm
from dashboard.user_admin.services import cnts


@login_required(login_url='sign-in')
def home(requests):
    member = Member.objects.filter(user=requests.user).first()
    if member.permission != 3:
        return redirect('home')

    ctx = {
        "cnts": cnts(),
        'member': member
    }

    return render(requests, 'admin/main.html', ctx)


@login_required(login_url='sign-in')
def manage_group(requests, group_id=None):
    member = Member.objects.filter(user=requests.user).first()
    if member.permission != 3:
        return redirect('home')

    if group_id:
        group = Group.objects.filter(id=group_id).first()
        if group:
            ctx = {
                'group': group,
                "position": "one"
            }
            return render(requests, 'admin/groups.html', ctx)

    groups = Group.objects.all().order_by('-pk')
    ctx = {
        'groups': groups,
        'position': 'list'
    }
    return render(requests, 'admin/groups.html', ctx)


@login_required(login_url='sign-in')
def manege_student(requests):
    member = Member.objects.filter(user=requests.user).first()
    if member.permission != 3:
        return redirect('home')
    members = Member.objects.filter(is_student=True).order_by('-pk')
    ctx = {
        'members': members,
        'position': 'list',
        'pos': 'st',

    }
    return render(requests, 'admin/member.html', ctx)


@login_required(login_url='sign-in')
def interested(requests, pk=None, contac_id=None):
    member = Member.objects.filter(user=requests.user).first()
    if member.permission != 3:
        return redirect('home')
    if pk:
        ins = Interested.objects.filter(id=pk).first()
        inst = Interested.objects.all()
        if not ins:
            ctx = {
                'intres': inst,
                'error': True
            }
            return render(requests, 'admin/instres.html', ctx)
        ins.view = True
        ins.save()
        ctx = {
            'inst': ins,
            'position': "one"
        }
        return render(requests, 'admin/instres.html', ctx)

    elif contac_id:
        ins = Interested.objects.filter(id=contac_id).first()
        inst = Interested.objects.all()
        if not ins:
            ctx = {
                'intres': inst,
                'error': True
            }
            return render(requests, 'admin/instres.html', ctx)
        ins.contacted = True
        ins.save()
        return redirect('admin-interested')

    else:
        inst = Interested.objects.all()
        ctx = {
            'intres': inst
        }

        return render(requests, 'admin/instres.html', ctx)


@login_required(login_url='sign-in')
def manage_mentor(requests, _id=None, edit_id=None):
    member = Member.objects.filter(user=requests.user).first()
    if member.permission != 3:
        return redirect('home')
    if edit_id:
        member = Member.objects.filter(pk=edit_id).first()
        if not member:
            members = Member.objects.filter(is_student=False).order_by('-pk')
            ctx = {
                'members': members,
                'position': 'list',
                "error": True
            }
            return render(requests, 'admin/member.html', ctx)
        teacher_form = MemberChangeForm(requests.POST or None, instance=member)
        if teacher_form.is_valid():
            teacher_form.save()
            return redirect('home')

        ctx = {
            "form": teacher_form,
            "member": member
        }
        return render(requests, 'admin/member.html', ctx)

    elif not _id:
        members = Member.objects.filter(is_student=False).order_by('-pk')
        ctx = {
            'members': members,
            'position': 'list'
        }
        return render(requests, 'admin/member.html', ctx)
    else:
        member = Member.objects.filter(pk=_id).first()
        if not member:
            members = Member.objects.filter(is_student=False).order_by('-pk')
            ctx = {
                'members': members,
                'position': 'list',
                "error": True
            }
            return render(requests, 'admin/member.html', ctx)

    ctx = {
        'position': 'one',
        "member": member

    }
    return render(requests, 'admin/member.html', ctx)


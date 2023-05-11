from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from dashboard.models.extra import Member, Group, Interested, Course, GroupStudent
from dashboard.user_admin.forms import MemberChangeForm, PasswordForm, CourseForm, GrStForm, GroupForm
from dashboard.user_admin.services import cnts, gcnt
from hashlib import sha1, sha256


@login_required(login_url='sign-in')
def home(requests):
    member = Member.objects.filter(user=requests.user).first()
    if not member or member.permission != 3:
        return redirect('home')

    new_joined = Member.objects.filter(permission=0).order_by('-pk')
    cnt = new_joined.count()
    ctx = {
        "cnts": cnts(),
        'member': member,
        "new_joined": new_joined,
        "cnt_joined": cnt - 3 if cnt > 3 else cnt - 2 if 4 > cnt > 2 else cnt - 1 if 2 > cnt > 0 else 0
    }

    return render(requests, 'admin/main.html', ctx)


@login_required(login_url='sign-in')
def manage_group(requests, group_id=None, status=None, student_id=None, _id=None):
    member = Member.objects.filter(user=requests.user).first()
    if not member or member.permission != 3:
        return redirect('home')

    if status == 201:  # status -> HTTP RESPONSE statuses 201-add, 99-add student, 1,2,3-group statuses
        group = Group.objects.filter(id=group_id).first()
        form = GroupForm(requests.POST or None, instance=group)
        ctx = {"group": group, "member": member, "form": form, "position": "add"}
        if form.is_valid():
            form.save()
            return redirect('admin-group-one', group_id=group_id)
        else:
            for i, j in form.errors.items():
                ctx['error'] = i
                break
        return render(requests, 'admin/groups.html', ctx)

    elif group_id:
        group = Group.objects.filter(id=group_id).first()
        if group:
            if student_id:
                gs = GroupStudent.objects.filter(group=group, student_id=student_id).first()
                None if not gs else gs.delete()
            elif status == 99:
                form = GrStForm(requests.POST or None, group=group)
                ctx = {"group": group, "member": member, "form": form, "position": "gr"}
                if form.is_valid():
                    form.save()
                    return redirect('admin-group-one', group_id=group_id)
                else:
                    for i, j in form.errors.items():
                        ctx['error'] = i
                        break
                return render(requests, 'admin/groups.html', ctx)

        queryset = GroupStudent.objects.select_related('group').filter(group=group)
        members = [x.student for x in queryset]
        ctx = {
            'group': group,
            "position": "one",
            "member": member,
            'members': members
        }
        return render(requests, 'admin/groups.html', ctx)


    elif status:
        groups = Group.objects.filter(status=status).order_by('-pk')
        ctx = {
            'groups': groups,
            'position': 'list',
            "member": member
        }
        return render(requests, 'admin/groups.html', ctx)
    ctx = {
        "member": member,
        'position': 'main',
        'gcnt': gcnt(),
    }

    return render(requests, 'admin/groups.html', ctx)


@login_required(login_url='sign-in')
def manege_student(requests, permission=None):
    member = Member.objects.filter(user=requests.user).first()
    if not member or member.permission != 3:
        return redirect('home')
    if permission == 0:
        members = Member.objects.filter(permission=0).order_by('-pk')
        ctx = {
            'members': members,
            'position': 'list',
            'pos': 'news',
            "member": member

        }
        return render(requests, 'admin/member.html', ctx)
    members = Member.objects.filter(is_student=True).order_by('-pk')

    ctx = {
        'members': members,
        'position': 'list',
        'pos': 'st',
        "member": member

    }
    return render(requests, 'admin/member.html', ctx)


@login_required(login_url='sign-in')
def interested(requests, pk=None, contac_id=None):
    member = Member.objects.filter(user=requests.user).first()
    if not member or member.permission != 3:
        return redirect('home')
    if pk:
        ins = Interested.objects.filter(id=pk).first()
        inst = Interested.objects.all().order_by('-pk')
        if not ins:
            ctx = {
                'intres': inst,
                'error': True,
                "member": member
            }
            return render(requests, 'admin/instres.html', ctx)
        ins.view = True
        ins.save()
        ctx = {
            'inst': ins,
            'position': "one",
            "member": member
        }
        return render(requests, 'admin/instres.html', ctx)

    elif contac_id:
        ins = Interested.objects.filter(id=contac_id).first()
        inst = Interested.objects.all().order_by('-pk')
        if not ins:
            ctx = {
                'intres': inst,
                'error': True,
                "member": member
            }
            return render(requests, 'admin/instres.html', ctx)
        ins.contacted = True
        ins.who_contacted = member
        ins.save()
        return redirect('admin-interested')

    else:
        inst = Interested.objects.all().order_by('-pk')
        ctx = {
            'intres': inst,
            "member": member
        }

        return render(requests, 'admin/instres.html', ctx)


@login_required(login_url='sign-in')
def manage_mentor(requests, _id=None, edit_id=None):
    member = Member.objects.filter(user=requests.user).first()
    if not member or member.permission != 3:
        return redirect('home')
    if edit_id:
        mb = Member.objects.filter(pk=edit_id).first()
        if not mb:
            members = Member.objects.filter(is_student=False).order_by('-pk')
            ctx = {
                'members': members,
                'member': member,
                'mb': mb,
                'position': 'list',
                "error": True,

            }
            return render(requests, 'admin/member.html', ctx)
        teacher_form = MemberChangeForm(requests.POST or None, instance=mb)
        if teacher_form.is_valid():
            teacher_form.save()
            return redirect('home')

        ctx = {
            "form": teacher_form,
            "member": member,
            'pos': 'st' if mb.is_student else 'all'
        }
        return render(requests, 'admin/member.html', ctx)

    elif not _id:
        members = Member.objects.filter(is_student=False).order_by('-pk')
        ctx = {
            'members': members,
            "member": member,
            'position': 'list'
        }
        return render(requests, 'admin/member.html', ctx)
    else:
        member = Member.objects.filter(pk=_id).first()
        if not member:
            members = Member.objects.filter(is_student=False).order_by('-pk')
            ctx = {
                'members': members,
                'member': member,
                'position': 'list',
                "error": True
            }
            return render(requests, 'admin/member.html', ctx)

    ctx = {
        'position': 'one',
        "member": member

    }
    return render(requests, 'admin/member.html', ctx)


@login_required(login_url='sign-in')
def manage_course(requests, pk=None, edit_id=None, del_id=None):
    member = Member.objects.filter(user=requests.user).first()
    if not member or member.permission != 3:
        return redirect('home')

    ctx = {
        "member": member
    }
    if del_id:
        course = Course.objects.filter(id=del_id).first()
        if not course:
            return redirect('admin-course')
        course.delete()
        return redirect('admin-course')

    if edit_id or edit_id == 0:
        course = Course.objects.filter(id=edit_id).first()
        form = CourseForm(requests.POST or None, instance=course)
        if form.is_valid():
            form.save()
            return redirect('admin-course')

        ctx = {
            "member": member,
            "form": form,
            "position": 'edit'
        }
        return render(requests, 'admin/course.html', ctx)
    if pk:
        course = Course.objects.filter(pk=pk).first()
        if not course:
            return redirect('admin-course')

        groups = Group.objects.filter(course=course)

        ctx.update({
            'position': 'one',
            'root': course,
            "groups": groups
        })

    else:
        ctx['position'] = 'list'
        ctx['courses'] = Course.objects.all()

    return render(requests, 'admin/course.html', ctx)


@login_required(login_url='sign-in')
def change_pass(requests):
    member = Member.objects.filter(user=requests.user).first()
    if not member or member.permission != 3:
        return redirect('home')

    form = PasswordForm(requests.POST or None)
    ctx = {
        "member": member,
        "form": form
    }
    if form.is_valid():
        pas = requests.POST.get("password")
        if pas != requests.POST.get("re_password"):
            ctx.update({
                "error": "re"
            })
            return render(requests, 'settings/change_pas.html', ctx)

        user = Member.objects.get(id=int(requests.POST.get("user")))
        user.user.set_password(pas)
        user.user.save()
        ctx.update({
            "success": True
        })
        return render(requests, 'settings/change_pas.html', ctx)

    else:
        print(form.errors)

    return render(requests, 'settings/change_pas.html', ctx)

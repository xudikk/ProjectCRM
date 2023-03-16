from django.shortcuts import render, redirect


def st_index(requests):
    if requests.user.is_anonymous:
        return redirect('sign-in')

    return render(requests, 'student/index.html', {})


from django.shortcuts import render


def default_login(request):
    return render(request=request, template_name="auth/login.html")

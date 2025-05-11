from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import authenticate
import socket
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import login,logout

# Create your views here.
def index(request):
    return render(request, 'main/index.html')

def about_us(request):
    return render(request, 'main/about.html')

def contact_us(request):
    return render(request, 'main/contact.html')

def doctor_list(request):
    return render(request, 'main/doctor.html')

def department_list(request):
    return render(request, 'main/dep.html')

def services(request):
    return render(request, 'main/services.html')

@csrf_exempt
def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return HttpResponse(
                status=204,
                headers={
                    'HX-Redirect': "/"
                }
            )
        else:
            return HttpResponse("""<div class="alert alert-danger alert-dismissible fade show mt-2" role="alert">
                    <strong>Warning!</strong> Invalid username or password!
                    <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
                </div>""")

    return render(request, 'main/login.html')

def register(request):
    return render(request, 'main/register.html')
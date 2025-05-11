from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import authenticate
import socket
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import login,logout
from core.forms import CustomUserRegistrationForm
from django.shortcuts import redirect

# Create your views here.


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


def register_view(request):
    form = CustomUserRegistrationForm(request.POST or None, request.FILES or None)
    if request.method == "POST":
        if form.is_valid():
            form.save()
            return HttpResponse("""<div class="alert alert-success alert-dismissible fade show mt-2" role="alert">
                                <strong>Success!</strong> A link to set your password has been sent to your email. Please check your inbox (or spam folder) and follow the instructions to set your new password.
                                <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
                            </div>
                            """)
        else:
            return HttpResponse(f"""<div class="alert alert-danger alert-dismissible fade show mt-2" role="alert">
                    <strong>Warning!</strong> {form.errors}
                    <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
                </div>""")
    else:
        form = CustomUserRegistrationForm()
    return render(request, "main/partials/form.html", {"form": form})

def logout_view(request):
    logout(request)
    return redirect('/')

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

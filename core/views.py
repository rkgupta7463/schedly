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

def load_role_specific_fields(request):
    role = request.GET.get('role')
    print("Raw role:", role)

    form = CustomUserRegistrationForm()
    fields = []

    try:
        role = int(role)  # Convert from string to integer
        if role in [2, 3]:  # Doctor or Nurse
            fields = [form[f] for f in [
                'full_name', 'email', 'phone', 'gender',
                'specialization', 'qualification_level', 'experience_years',
                'registration_number', 'consultation_fee', 'available_from',
                'available_to', 'available_days', 'clinic_location'
            ]]
        elif role == 1:  # Patient
            fields = [form[f] for f in [
                'full_name', 'email', 'phone', 'gender', 'date_of_birth',
                'address', 'city', 'state', 'country', 'pincode',
                'blood_group', 'emergency_contact', 'insurance_provider',
                'insurance_number'
            ]]
    except (ValueError, TypeError):
        print("Invalid role received:", role)

    return render(request, "main/plugins/role_specific_fields.html", {'fields': fields})



@csrf_exempt
def register_user_view(request):
    if request.method == "POST":
        form = CustomUserRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            return HttpResponse("""<div class="alert alert-success alert-dismissible fade show mt-2" role="alert">
                        <strong>Success!</strong> A link to set your password has been sent to your email. Please check your inbox (or spam folder) and follow the instructions to set your new password.
                        <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
                        </div>
                    """)
            # login(request, user)
            # return HttpResponse(status=204, headers={'HX-Redirect': '/'})
        else:
            return HttpResponse(f"""<div class="alert alert-warning alert-dismissible fade show mt-2" role="alert">
                        <strong>Warning!</strong> {form.errors}
                        <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
                        </div>
                    """)

    form = CustomUserRegistrationForm()
    return render(request, 'main/register.html', {'form': form})


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

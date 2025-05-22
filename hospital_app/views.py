from django.shortcuts import render,redirect
from .forms import *
from .models import *
from django.contrib.auth.decorators import login_required

def book_appoinment(request):
    if request.method == "POST":
        form = AppointmentForm(request.POST)
        if form.is_valid():
            form.save()
            print("form has submitted!!")
            return redirect('home')
        else:
            return render(request, 'book_appoinment.html', {'form': form})
    else:
        form = AppointmentForm()
    
    return render(request, 'main/partials/appoinment_form.html', {'form': form})




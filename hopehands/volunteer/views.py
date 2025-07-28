from django.shortcuts import render, redirect
from .forms import VolunteerForm

def volunteer_signup(request):
    if request.method == 'POST':
        form = VolunteerForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('success')
    else:
        form = VolunteerForm()
    return render(request, 'volunteer/signup.html', {'form': form})

def success(request):
    return render(request, 'volunteer/success.html')

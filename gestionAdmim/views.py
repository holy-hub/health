from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect, get_object_or_404

from authentification.models import Medecin, Pharmacien

# Create your views here.
def log_in(request):
    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        print(username, password)
        user = authenticate(request, username=username, password=password)
        print(f"\n{username}, {password}\n{user}\n")
        if user is not None:
            user = User.objects.get(username=username)
            if user.is_staff:
                login(request, user)
        return redirect('dashboard_adm')
    context = {
        'title': 'Admin Login',
    }
    return render(request, 'adm/auth.html', context)

def sign(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password = make_password(password)

        user = User.objects.create(username=username, email=email, password=password)
        user.is_staff = True
        user.is_superuser = True
        user.save()
        # return redirect('dashboard_adm')
    return redirect('connex')

def dashboard_adm(request):
    ph = Pharmacien.objects.filter(approuverPharmacien=False, verifierPharmacien=False).all()
    med = Medecin.objects.filter(approuverMedecin=False, verifierMedecin=False).all()

    context = {
        'title': 'Profils',
        'pharmaciens': ph,
        'medecins': med,
    }
    return render(request, 'adm/dashboard.html', context)

def approve(request, status, id):
    if status == 'medecin':
        profile = get_object_or_404(Medecin, pk=id)
    else:
        profile = get_object_or_404(Pharmacien, pk=id)

    if request.method == 'POST':
        response = request.POST.get('response', '')
        if status == "medecin":
            profile.verifierMedecin = True
            profile.approuverMedecin = (response == 'yes')
        else:
            profile.verifierPharmacien = True
            profile.approuverPharmacien = (response == 'yes')
        profile.save()
        return redirect('dashboard_adm')
    context = {
        'title': 'ApprobatioApprobation ADMIN',
        'm': profile, 
        's': status,
    }
    return render(request, 'adm/approuve.html', context)

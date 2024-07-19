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

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard_adm')
    context = {
        'title': 'Admin Login'
    }
    return render(request, 'adm/auth.html', context)

def sign(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password = make_password(password)

        user = User.objects.create_superuser(username=username, email=email, password=password)
        user.save()
        return redirect('dashboard_adm')
    return redirect('connnex')

def dashboard_adm(request):
    ph = Pharmacien.objects.filter(approuverPharmacien=False).all()
    med = Medecin.objects.filter(approuverMedecin=False).all()

    context = {
        'title': 'Approuver profils',
        'pharmaciens': ph,
        'medecins': med,
    }
    return render(request, 'approuve.html', context)

def approve(request, status, id):
    if request.method == 'POST':
        if status == 'medecin':
            response = request.POST.get('response', '')
            if response == 'yes':
                m = get_object_or_404(Medecin, pk=id)
                if m: m.approuverMedecin = True
        elif status == 'pharmacien':
            response = request.POST.get('response', '')
            if response == 'yes':
                p = get_object_or_404(Pharmacien, pk=id)
                if p: p.approuverPharmacien = True
    return redirect('dashboard_adm')
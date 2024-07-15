from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from medecin.models import Prescription
from .models import *

# Create your views here.
# PATIENT
# @login_required
def dashboard(request):
    # rdv = Appointement.objects.filter(patient=request.user).all()
    # nb_rdv = len(rdv)
    context = {
        'title': 'Patient ', # + request.user.first_name,
        # 'nombres-de-rdv': nb_rdv,
    }
    return render(request, 'patient/dashboard.html', context)

@login_required
def my_appointement(request):
    rdv = Appointement.objects.filter(patient=request.user).all()
    context = {
        'title': 'Patient ' + request.user.first_name,
        'rdvs': rdv,
    }
    return render(request, 'patient/my_appointement.html', context)

@login_required
def ask_appointement(request, med_id):
    if request.method == 'POST':
        medecin = Medecin.objects.get(pk=med_id)
        Appointement.objects.get_or_create(patient=request.user, medecin=medecin)

@login_required
def prescription(request):
    ordonnances = Prescription.objects.filter(patient=request.user).all()
    context = {
        'title': 'Mes ordonnances',
        'ordonnances': ordonnances,
    }
    return render(request, 'patient/my_prescription.html', context)

def all_medecin(request):
    medecins = Medecin.objects.all()
    context = {
        'title': 'Tous les medecins',
        'medecins': medecins,
    }
    return render(request, 'patient/medecins.html', context)

@login_required
def prescription_name(request, prsc_name):
    ordonnance = Prescription.objects.get(title=prsc_name)
    context = {
        'title': 'Ordonnance ' + ordonnance.title,
        'ordonnances': ordonnance,
    }
    return render(request, 'patient/myOne_prescription.html', context)

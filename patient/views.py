from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from medecin.models import Prescription
from .models import *

# Create your views here.
# PATIENT
@login_required
def dashboard(request):
    rdv = Appointement.objects.filter(patient=request.user).all()
    nb_rdv = len(rdv)
    context = {
        'title': 'Utilisateur ' + request.user.user.username,
        'nombres-de-rdv': nb_rdv,
    }
    return render(request, 'dashboard.html', context)

@login_required
def my_appointement(request):
    rdv = Appointement.objects.filter(patient=request.user).all()
    context = {
        'title': 'Utilisateur ' + request.user.user.username,
        'rdvs': rdv,
    }
    return render(request, 'my_appointement.html', context)

def ask_appointement(request, doc_id):
    if request.method == 'POST':
        medecin = Utilisateur.objects.get(pk=doc_id)
        Appointement.objects.get_or_create(patient=request.user, medecin=medecin).save()

@login_required
def prescription(request):
    ordonnances = Prescription.objects.filter(patient=request.user).all()
    context = {
        'title': 'Mes ordonnances',
        'ordonnances': ordonnances,
    }
    return render(request, 'my_prescription.html', context)

@login_required
def prescription_name(request, prsc_name):
    ordonnance = Prescription.objects.get(title=prsc_name)
    context = {
        'title': 'Ordonnance ' + ordonnance.title,
        'ordonnances': ordonnance,
    }
    return render(request, 'myOne_prescription.html', context)

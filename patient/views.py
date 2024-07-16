from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from medecin.models import Advice, CarnetSante, Facture, Prescription
from pharmacie.models import Maladie
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
    STATUS_CHOICE = (
        ('accepte', 'ACCEPTÉ'),
        ('refuse', 'REFUSÉ'),
        ('annule', 'ANNULÉ'),
        ('en attente', 'EN ATTENTE'),
    )

    rdv_accepte = Appointement.objects.filter(patient=request.user, status=STATUS_CHOICE[0]).all()
    rdv_refuse = Appointement.objects.filter(patient=request.user, status=STATUS_CHOICE[1]).all()
    rdv_annule = Appointement.objects.filter(patient=request.user, status=STATUS_CHOICE[2]).all()
    rdv_en_attente = Appointement.objects.filter(patient=request.user, status=STATUS_CHOICE[3]).all()

    conseils, maladies = list(Advice.objects.all()), list(Maladie.objects.all())
    three_conseils = random.sample(conseils, 3) if len(conseils) > 3 else conseils
    three_maladies = random.sample(maladies, 3) if len(maladies) > 3 else maladies

    context = {
        'title': 'Patient ' + request.user.first_name,
        'rdv_acceptes': rdv_accepte,
        'rdv_refuses': rdv_refuse,
        'rdv_annules': rdv_annule,
        'rdv_en_attentes': rdv_en_attente,
        'conseils': three_conseils,
        'maladies': three_maladies,
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

@login_required
def prescription_name(request, prsc_name):
    ordonnance = Prescription.objects.get(title=prsc_name)
    context = {
        'title': 'Ordonnance ' + ordonnance.title,
        'ordonnances': ordonnance,
    }
    return render(request, 'patient/myOne_prescription.html', context)

def all_medecin(request):
    medecins = Medecin.objects.all()
    context = {
        'title': 'Tous les medecins',
        'medecins': medecins,
    }
    return render(request, 'patient/medecins.html', context)

@login_required
def monCarnet(request):
    carnet = CarnetSante.objects.get(patient=request.user)
    first_data = carnet.hospitalisations[:14]
    last_data = carnet.hospitalisations[14:]
    context = {
        'title': 'Mon Carnet de Sante',
        'monCarnet': carnet,
        'first_data': first_data,
        'last_data': last_data,
    }
    return render(request, 'patient/carnet_de_sante.html', context)

@login_required
def factures(request):
    factures = Facture.objects.filter(patient=request.user).all()
    conseils, maladies = list(Advice.objects.all()), list(Maladie.objects.all())
    three_conseils = random.sample(conseils, 3) if len(conseils) > 3 else conseils
    three_maladies = random.sample(maladies, 3) if len(maladies) > 3 else maladies

    context = {
        'title': 'Mes Factures',
        'factures': factures,
        'conseils': three_conseils,
        'maladies': three_maladies,
    }
    return render(request, 'patient/facture.html', context)

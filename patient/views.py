from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from medecin.models import Advice, CarnetSante, Facture, Prescription
from pharmacie.models import Maladie
from django.contrib import messages
from .models import *

# Create your views here.
# PATIENT
@login_required
def dashboard(request):
    patient = get_object_or_404(Patient, pk=request.user.id)
    rdv = Appointement.objects.filter(patient=patient, status="EN ATTENTE").all()
    rdv_a = Appointement.objects.filter(patient=patient, status="ACCEPTÉ").all()
    rdv_r = Appointement.objects.filter(patient=patient, status="REFUSÉ").all()
    rdv_an = Appointement.objects.filter(patient=patient, status="ANNULÉ").all()
    nb_rdv, nb_rdv_a, nb_rdv_r, nb_rdv_an = len(rdv), len(rdv_a), len(rdv_r), len(rdv_an)
    context = {
        'title': 'Patient ' + patient.username,
        'date': patient.date_joined.strftime('%b %Y'),
        'nb_rdv': nb_rdv,
        'nb_rdv_a': nb_rdv_a,
        'nb_rdv_r': nb_rdv_r,
        'nb_rdv_an': nb_rdv_an,
        'rdv_a': rdv_a,
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

    rdv_accepte = Appointement.objects.filter(patient=request.user, status=STATUS_CHOICE[0][1]).all()
    rdv_refuse = Appointement.objects.filter(patient=request.user, status=STATUS_CHOICE[1][1]).all()
    rdv_annule = Appointement.objects.filter(patient=request.user, status=STATUS_CHOICE[2][1]).all()
    rdv_en_attente = Appointement.objects.filter(patient=request.user, status=STATUS_CHOICE[3][1]).all()

    conseils, maladies = list(Advice.objects.all()), list(Maladie.objects.all())
    three_conseils = random.sample(conseils, 3) if len(conseils) > 3 else conseils
    three_maladies = random.sample(maladies, 3) if len(maladies) > 3 else maladies

    context = {
        'title': 'Patient ' + request.user.first_name,
        'date': request.user.date_joined.strftime('%b %Y'),
        'rdv_acceptes': rdv_accepte,
        'rdv_refuses': rdv_refuse,
        'rdv_annules': rdv_annule,
        'rdv_en_attentes': rdv_en_attente,
        'conseils': three_conseils,
        'maladies': three_maladies,
    }
    return render(request, 'patient/my_appointement.html', context)

@login_required
def ask_appointement(request, id):
    if request.method == 'POST':
        medecin = Medecin.objects.get(pk=id)
        patient = Patient.objects.get(pk=request.user.id)
        Appointement.objects.create(patient=patient, medecin=medecin)
        messages.success(request, "Demande envoyee avec succes.")
    return redirect('all_medecin')

@login_required
def motif(request):
    if request.method == 'POST':
        patient = get_object_or_404 (Patient, pk=request.user.id)
        rdv = Appointement.objects.filter(patient=patient).last()
        motif = request.POST.get('motif')
        rdv.motif = motif
        return redirect('dashboard_p')
    return redirect('all_medecin')

@login_required
def prescription(request):
    ordonnances = Prescription.objects.filter(patient=request.user).all()
    context = {
        'title': 'Mes ordonnances',
        'date': request.user.date_joined.strftime('%b %Y'),
        'ordonnances': ordonnances,
    }
    return render(request, 'patient/my_prescription.html', context)

@login_required
def prescription_name(request, id):
    ordonnance = Prescription.objects.get(title=id)
    context = {
        'title': 'Ordonnance ' + ordonnance.title,
        'date': request.user.date_joined.strftime('%b %Y'),
        'ordonnances': ordonnance,
    }
    return render(request, 'patient/myOne_prescription.html', context)

def all_medecin(request):
    medecins = Medecin.objects.all()
    context = {
        'title': 'Tous les medecins',
        'date': request.user.date_joined.strftime('%b %Y'),
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
        'date': request.user.date_joined.strftime('%b %Y'),
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
        'date': request.user.date_joined.strftime('%b %Y'),
        'factures': factures,
        'conseils': three_conseils,
        'maladies': three_maladies,
    }
    return render(request, 'patient/facture.html', context)

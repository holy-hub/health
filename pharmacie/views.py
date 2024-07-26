import random
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, redirect, get_object_or_404

from authentification.models import Archive, Pharmacien, Utilisateur
from .models import *

# Create your views here.
def is_patient(user):
    user = Utilisateur.objects.get(id=user.id)
    return user.is_patient

def is_doctor(user):
    user = Utilisateur.objects.get(id=user.id)
    return user.is_medecin

def is_pharmacist(user):
    user = Utilisateur.objects.get(id=user.id)
    return user.is_pharmacien

# PHARMACIE
@user_passes_test(is_pharmacist)
@login_required
def dashboard(request):
    try:
        pharmacien = get_object_or_404(Pharmacien, pk=request.user.id)
        medications = pharmacien.pharmacie.medications.all() if pharmacien.pharmacie else []
    except Pharmacien.DoesNotExist:
        medications = [] # Handle the case where the Pharmacien object does not exist
    maladies = list(Maladie.objects.all())
    three_maladies = random.sample(maladies, 3) if len(maladies) > 3 else maladies

    context = {
        'title': 'Pharmacien ' + pharmacien.username,
        'pharmacie': pharmacien.pharmacie,
        'date': pharmacien.date_joined.strftime('%b %Y'),
        'nb_medocs': len(medications),
        'maladies': three_maladies,
    }
    return render(request, 'pharmacien/dashboard.html', context)

@user_passes_test(is_pharmacist)
@login_required
def creaPhar(request):
    if request.method == "POST":
        nom = request.POST.get('nom', '')
        location = request.POST.get('location', '')
        description = request.POST.get('description', '')
        ph = get_object_or_404(Pharmacien, pk=request.user.id)
        
        if ph.pharmacie:
            pass
        else:
            pcie = Pharmacie.objects.create(nom=nom, location=location, description=description)
            pcie.save()
            ph.pharmacie = pcie
            ph.save()
        return redirect('dashboard_ph')
    context = {
        'title': 'Ajout de Pharmacie',
    }
    return render(request, 'pharmacien/create.html', context)

@user_passes_test(is_pharmacist)
@login_required
def readMyPhar(request):
    pharmacien = get_object_or_404(Pharmacien, pk=request.user.id)
    pharmacie = pharmacien.pharmacie
    context = {
        'title'     : 'informations de Pharmacie',
        'pharmacie' : pharmacie,
    }
    return render(request, 'pharmacien/read.html', context)

def readPhar(request, id):
    pharmacie = get_object_or_404(Pharmacie, pk=id)
    context = {
        'title'     : 'informations de Pharmacie',
        'pharmacie' : pharmacie,
    }
    return render(request, 'pharmacien/read.html', context)

def readAllPhar(request):
    pharmacies = Pharmacie.objects.all()
    context = {
        'title'      : 'informations de Pharmacie',
        'pharmacies' : pharmacies,
    }
    return render(request, 'pharmacien/readAll.html', context)

@user_passes_test(is_pharmacist)
@login_required
def updPhar(request):
    if request.method == "PUT":
        pharmacien = get_object_or_404(Pharmacien, pk=request.user.id)
        pharmacie = pharmacien.pharmacie
        nom = request.POST.get('nom', '')
        location = request.POST.get('location', '')
        description = request.POST.get('description', '')

        if pharmacie == pharmacien.pharmacie:
            pharmacie.nom, pharmacie.location, pharmacie.description = nom, location, description
            pharmacie.save()
            return redirect('dashboard_ph')
    context = {
        'title' : 'Mise a jour de Pharmacie',
        'ph' : pharmacie,
    }
    return render(request, 'pharmacien/update.html', context)

@user_passes_test(is_pharmacist)
@login_required
def delPhar(request):
    if request.method == "POST":
        ph = get_object_or_404(Pharmacien, pk=request.user.id)
        pcie = ph.pharmacie
        Archive.objects.create(content_object=pcie, archive_by=ph)
        pcie.delete()
        return redirect('dashboard_ph')

# MALADIE
@user_passes_test(is_pharmacist)
@login_required
def creaIll(request):
    if request.method == "POST":
        nom = request.POST.get('nom', '')
        nom_scientiste = request.POST.get('nom_scientiste', '')
        symptomes = request.POST.get('symptomes', '')
        causes = request.POST.get('causes', '')
        consequences = request.POST.get('consequences', '')
        prevention = request.POST.get('prevention', '')
        disease_types = request.POST.get('disease_types', '')
        
        Maladie.objects.create(nom=nom, disease_types=disease_types, nom_scientiste=nom_scientiste, symptomes=symptomes, causes=causes, consequences=consequences, prevention=prevention).save()
        return redirect('dashboard_ph')
    context = {
        'title': 'Ajout de Maladie',
    }
    return render(request, 'pharmacien/creaMal.html', context)

def readIll(request, id):
    maladie = get_object_or_404(Maladie, pk=id)
    context = {
        'title' : 'informations de la Maladie',
        'maladie' : maladie,
    }
    return render(request, 'pharmacien/readMal.html', context)

def readAllIll(request):
    maladies = Maladie.objects.all()
    context = {
        'title'    : 'informations des Maladies',
        'maladies' : maladies,
    }
    return render(request, 'pharmacien/readAllMal.html', context)

@user_passes_test(is_pharmacist)
@login_required
def updIll(request, id):
    if request.method == "PUT":
        maladie = get_object_or_404(Maladie, pk=id)
        nom = request.POST.get('nom', '')
        nom_scientiste = request.POST.get('nom_scientiste', '')
        symptomes = request.POST.get('symptomes', '')
        causes = request.POST.get('causes', '')
        consequences = request.POST.get('consequences', '')
        prevention = request.POST.get('prevention', '')
        disease_types = request.POST.get('disease_types', '')

        if maladie:
            maladie.nom, maladie.causes, maladie.disease_types, maladie.nom_scientiste, maladie.consequences, maladie.symptomes, maladie.prevention = nom, causes, disease_types, nom_scientiste, consequences, symptomes, prevention
            maladie.save()
            return redirect('dashboard_ph')
    context = {
        'title' : 'Mise a jour de la Maladie',
        'maladie' : maladie,
    }
    return render(request, 'pharmacien/updateIll.html', context)

@login_required
def delIll(request, id):
    if request.method == "POST":
        m = get_object_or_404(Maladie, pk=id)
        Archive.objects.create(archived_by=request.user, content_object=m).save()
        m.delete()

# MEDICATION
@user_passes_test(is_pharmacist)
@login_required
def creaMedoc(request):
    if request.method == "POST":
        nom  = request.POST.get('nom', '')
        prix = request.POST.get('prix', '')
        image = request.FILES.get('image', None)
        avantages = request.POST.get('avantages', '')
        inconvenients = request.POST.get('inconvenients', '')
        
        m = Medication.objects.create(nom=nom, avantages=avantages, prix=prix, inconvenients=inconvenients, image=image).save()
        if request.user.is_authenticated:
            ph = get_object_or_404(Pharmacien, pk=request.user.id)
            # ph.pharmacie.medications.add(m)
        return redirect('dashboard_ph')
    context = {
        'title': 'Ajout de Medicament',
    }
    return render(request, 'pharmacien/creaMedoc.html', context)

def readMedoc(request, id):
    medicament = get_object_or_404(Medication, pk=id)
    context = {
        'title'      : 'informations de Medication',
        'medicament' : medicament,
    }
    return render(request, 'pharmacien/readMedoc.html', context)

def readAllMedoc(request):
    medication = Medication.objects.all()
    context = {
        'title' : 'informations de Medication',
        'medications' : medication,
    }
    return render(request, 'pharmacien/readAllMedoc.html', context)

@user_passes_test(is_pharmacist)
@login_required
def updMedoc(request, id):
    if request.method == "PUT":
        medication = get_object_or_404(Medication, pk=id)
        nom  = request.POST.get('nom', '')
        prix = request.POST.get('prix', '')
        image = request.FILES.get('image', None)
        avantages = request.POST.get('avantages', '')
        inconvenients = request.POST.get('inconvenients', '')

        if medication.pharmacie.pharmacien == request.user:
            medication.nom, medication.image, medication.prix, medication.avantages, medication.inconvenients = nom, image, prix, avantages, inconvenients
            medication.save()
            return redirect('dashboard_ph')
    context = {
        'title' : 'Mise a jour de Medication',
        'medication' : medication,
    }
    return render(request, 'pharmacien/updateMedoc.html', context)

@user_passes_test(is_pharmacist)
@login_required
def delMedoc(request, id):
    if request.method == "POST":
        m =get_object_or_404(Medication, pk=id)
        Archive.objects.create(content_object=m, archived_by=request.user).save()
        m.delete()
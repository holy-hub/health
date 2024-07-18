from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from authentification.models import Archive
from .models import *

# Create your views here.
# PHARMACIE
# @login_required
def dashboard(request):
    pharmacie = Pharmacie.objects.get(pharmacien=request.user)
    medications = pharmacie.medications
    context = {
        'title': 'Pharmacien ' + request.user.username,
        'nb_medocs': len(medications),
    }
    return render(request, 'pharmacien/dashboard_ph.html', context)

# @login_required
def creaPhar(request):
    if request.method == "POST":
        nom = request.POST.get('nom', '')
        location = request.POST.get('location', '')
        description = request.POST.get('description', '')
        
        Pharmacie.objects.create(nom=nom, location=location, description=description, pharmacien=request.user).save()
        return redirect('dashboard_ph')
    context = {
        'title': 'Ajout de Pharmacie',
    }
    return render(request, 'pharmacien/create.html', context)

def readPhar(request, pha_name):
    pharmacie = Pharmacie.objects.get(nom=pha_name)
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

# @login_required
def updPhar(request, pha_name):
    if request.method == "PUT":
        pharmacie = Pharmacie.objects.get(nom=pha_name)
        nom      = request.POST.get('nom', '')
        location = request.POST.get('location', '')
        description = request.POST.get('description', '')

        if pharmacie.pharmacien == request.user:
            pharmacie.nom, pharmacie.location, pharmacie.description = nom, location, description
            pharmacie.save()
            return redirect('dashboard_ph')
    context = {
        'title'     : 'Mise a jour de Pharmacie',
        'pharmacie' : pharmacie,
    }
    return render(request, 'pharmacien/update.html', context)

# @login_required
def delPhar(request, pha_name):
    if request.method == "DEL":
        response = request.POST.get('response', '')
        if response == 'yes':
            ph = Pharmacie.objects.get(nom=pha_name)
            Archive.objects.create(content_object=ph, archive_by=request.user)
            ph.delete()

# MALADIE
# @login_required
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

def readIll(request, mal_name):
    maladie = Maladie.objects.get(nom=mal_name)
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

# @login_required
def updIll(request, mal_name):
    if request.method == "PUT":
        maladie = Maladie.objects.get(nom=mal_name)
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

# @login_required
def delIll(request, mal_name):
    if request.method == "DEL":
        response = request.POST.get('response', '')
        if response == 'yes':
            m = Maladie.objects.get(nom=mal_name)
            Archive.objects.create(archived_by=request.user, content_object=m).save()
            m.delete()

# MEDICATION
# @login_required
def creaMedoc(request):
    if request.method == "POST":
        nom  = request.POST.get('nom', '')
        prix = request.POST.get('prix', '')
        image = request.FILES.get('image', None)
        avantages = request.POST.get('avantages', '')
        inconvenients = request.POST.get('inconvenients', '')
        
        Pharmacie.objects.create(nom=nom, avantages=avantages, prix=prix, inconvenients=inconvenients, image=image).save()
        return redirect('dashboard_ph')
    context = {
        'title': 'Ajout de Medicament',
    }
    return render(request, 'pharmacien/creaMedoc.html', context)

def readMedoc(request, medoc_name):
    medicament = Medication.objects.get(nom=medoc_name)
    context = {
        'title'      : 'informations de Medication',
        'medicament' : medicament,
    }
    return render(request, 'pharmacien/readMedoc.html', context)

def readAllMedoc(request):
    medication = Medication.objects.all()
    context = {
        'title' : 'informations de Medication',
        'medication' : medication,
    }
    return render(request, 'pharmacien/readAllMedoc.html', context)

# @login_required
def updMedoc(request, medoc_name):
    if request.method == "PUT":
        medication = Medication.objects.get(nom=medoc_name)
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

# @login_required
def delMedoc(request, medoc_name):
    if request.method == "DEL":
        response = request.POST.get('response', '')
        if response == 'yes':
            m =Medication.objects.get(nom=medoc_name)
            Archive.objects.create(content_object=m, archived_by=request.user).save()
            m.delete()

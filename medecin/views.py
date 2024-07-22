from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test

from pharmacie.views import is_patient
from .models import *

# create your views here.
# MEDECIN
@login_required
def dashboard(request):
    medecin = get_object_or_404(Medecin, id=request.user.id)
    rdvs = Appointement.objects.filter(medecin=medecin, status='EN ATTENTE').all()
    rdva = Appointement.objects.filter(medecin=medecin, status='ACCEPTÉ').all()
    context = {
        'title': 'Medecin ' + medecin.username,
        'rdvs': rdvs,
        'rdva': rdva,
        'date': medecin.date_joined.strftime('%b %Y'),
    }
    return render(request, 'medecin/dashboard.html', context)

@login_required
def refuse(request, id):
    rdv = get_object_or_404(Appointement, pk=id)
    rdv.response(1)
    return redirect('dashboard_m')

@login_required
def prevu(request, id):
    rdv = get_object_or_404(Appointement, pk=id)
    if request.method == 'POST':
        date = request.POST.get('date')
        if date:
            rdv.date_rdv = date
            rdv.status = rdv.STATUS_CHOICE[0][1]  # Set status to "accepté"
            rdv.save()
    return redirect('dashboard_m')

@login_required
def uPrevu(request, id):
    rdv = get_object_or_404(Appointement, pk=id)
    if request.method == 'POST':
        date = request.POST.get('date')
        if date:
            rdv.date_rdv = date
            rdv.save()
    return redirect('dashboard_m')

"""
    Hospital CRUD
"""
@login_required
def creaHopital(request):
    if request.method == 'POST':
        nom = request.POST.get('nom', '')
        adresse = request.POST.get('adresse', '')
        localisation = request.POST.get('localisation', '')

        Hopital.objects.create(nom=nom, adresse=adresse, localisation=localisation).save()
        return redirect('dashboard_m')
    context = {
        'title': 'Ajouter Hopital',
    }
    return render(request, 'medecin/createHospital.html', context)

def readHopital(request, id):
    hospital = Hopital.objects.get(pk=id)
    context = {
        'title': 'Afficher Hopital',
        'hopital': hospital,
    }
    return render(request, 'medecin/updateHospital.html', context)

def readAllHopital(request):
    hospitals = Hopital.objects.all()
    context = {
        'title': 'Afficher Hopitaux',
        'hopitals': hospitals,
    }
    return render(request, 'medecin/updateHospital.html', context)

@login_required
def updHopital(request, id):
    hospital = Hopital.objects.get(pk=id)
    if request.method == 'PUT':
        nom = request.POST.get('nom', '')
        adresse = request.POST.get('adresse', '')
        localisation = request.POST.get('localisation', '')

        hospital.nom = nom
        hospital.adresse = adresse
        hospital.localisation = localisation
        hospital.save()
        return redirect('dashboard_m')
    context = {
        'title': 'Ajouter Hopital',
        'hopital': hospital,
    }
    return render(request, 'medecin/updateHospital.html', context)

@login_required
def delHopital(request, id):
    h = Hopital.objects.get(pk=id)
    Archive.objects.create(content_object=h, archived_by=request.user)
    h.delete()
    return redirect('dashboard_m')

"""
    Advice CRUD
"""
@login_required
def creaAdvice(request):
    if request.method == 'POST':
        title = request.POST.get('title', '')
        content = request.POST.get('content', '')
        ill = request.POST.get('ill', '')
        image = request.POST.get('image', '')

        Advice.objects.create(title=title, content=content, ill=ill, medecin=request.user, image=image).save()
        return redirect('dashboard_m')
    context = {
        'title': 'Ajouter Advice',
    }
    return render(request, 'medecin/createAdvice.html', context)

def readAdvice(request, adv_name):
    advice = Advice.objects.get(pk=adv_name)
    context = {
        'title': 'Ajouter Advice',
        'advice': advice,
    }
    return render(request, 'medecin/readAdvice.html', context)

def readAllAdvice(request):
    advice = Advice.objects.all()
    context = {
        'title': 'Afficher Advices',
        'advice': advice,
    }
    return render(request, 'medecin/readAllAdvice.html', context)

@login_required
def updAdvice(request, adv_name):
    advice = Advice.objects.get(pk=adv_name)
    if request.method == 'PUT':
        title = request.POST.get('title', '')
        content = request.POST.get('content', '')
        ill = request.POST.get('ill', '')
        image = request.POST.get('image', '')

        advice.title = title
        advice.content = content
        advice.ill = ill
        advice.image = image
        advice.save()
        return redirect('dashboard_m')
    context = {
        'title': 'Ajouter Advice',
        'advice': advice,
    }
    return render(request, 'medecin/updateAdvice.html', context)

@login_required
def delAdvice(request, adv_name):
    a = Advice.objects.get(pk=adv_name)
    Archive.objects.create(content_object=a, archived_by=request.user)
    a.delete()
    return redirect('dashboard_m')

"""
    Consigne CRUD
"""
@login_required
def creaConsigne(request):
    if request.method == 'POST':
        medication = request.POST.get('medication', '')
        posologie = request.POST.get('posologie', '')

        Consigne.objects.create(medication=medication, posologie=posologie).save()
        return redirect('dashboard_m')
    context = {
        'title': 'Ajouter Consigne',
    }
    return render(request, 'medecin/createConsigne.html', context)

def readConsigne(request, csg_name):
    consigne = Consigne.objects.get(pk=csg_name)
    context = {
        'title': 'Ajouter Consigne',
        'consigne': consigne,
    }
    return render(request, 'medecin/updateHospital.html', context)

def readAllConsigne(request):
    consignes = Consigne.objects.all()
    context = {
        'title': 'Afficher tous les Consignes',
        'consignes': consignes,
    }
    return render(request, 'medecin/readAllConsigne.html', context)

@login_required
def updConsigne(request, csg_name):
    consigne = Consigne.objects.get(pk=csg_name)
    if request.method == 'PUT':
        medication = request.POST.get('medication', '')
        posologie = request.POST.get('posologie', '')

        consigne.medication = medication
        consigne.posologie = posologie
        consigne.save()
        return redirect('dashboard_m')
    context = {
        'title': 'Modifier Consigne',
        'consigne': consigne,
    }
    return render(request, 'medecin/updateHospital.html', context)

@login_required
def delConsigne(request, csg_name):
    c = Consigne.objects.get(pk=csg_name)
    Archive.objects.create(content_object=c, archived_by=request.user)
    c.delete()
    return redirect('dashboard_m')

"""
    Prescription CRUD
"""
@login_required
def creaPrescription(request):
    if request.method == 'POST':
        temperature = request.POST.get('temperature', '')
        observation = request.POST.get('observation', '')
        consigne = request.POST.get('consigne', '')
        patient = request.POST.get('patient', '')

        Prescription.objects.create(temperature=temperature, observation=observation, consigne=consigne, patient=patient).save()
        return redirect('dashboard_m')
    context = {
        'title': 'Ajouter Prescription',
    }
    return render(request, 'medecin/createPrescription.html', context)

def readPrescription(request, prsc_title):
    prescription = Prescription.objects.get(pk=prsc_title)
    context = {
        'title': 'Afficher Prescription',
        'Prescription': prescription,
    }
    return render(request, 'medecin/readPrscription.html', context)

def readAllPrescription(request):
    prescriptions = Prescription.objects.all()
    context = {
        'title': 'Afficher Les Prescriptions',
        'prescriptions': prescriptions,
    }
    return render(request, 'medecin/readAllPrscription.html', context)

@login_required
def updPrescription(request, prsc_title):
    prescription = Prescription.objects.get(pk=prsc_title)
    if request.method == 'PUT':
        nom = request.POST.get('nom', '')
        adresse = request.POST.get('adresse', '')
        localisation = request.POST.get('localisation', '')

        prescription.nom = nom
        prescription.adresse = adresse
        prescription.localisation = localisation
        prescription.save()
        return redirect('dashboard_m')
    context = {
        'title': 'Ajouter Prescription',
        'Prescription': prescription,
    }
    return render(request, 'medecin/updatePrescription.html', context)

@login_required
def delPrescription(request, prsc_title):
    p = Hopital.objects.get(pk=prsc_title)
    Archive.objects.create(content_object=p, archived_by=request.user)
    p.delete()
    return redirect('dashboard_m')

"""
    Speciality CRUD
"""
@login_required
def creaSpeciality(request):
    if request.method == 'POST':
        nom = request.POST.get('nom', '')
        description = request.POST.get('description', '')

        Speciality.objects.create(nom=nom, description=description).save()
        return redirect('dashboard_m')
    context = {
        'title': 'Ajouter Speciality',
    }
    return render(request, 'medecin/createSpeciality.html', context)

def readSpeciality(request, spc_name):
    speciality = Speciality.objects.get(title=spc_name)
    context = {
        'title': 'Ajouter Speciality',
        'Speciality': speciality,
    }
    return render(request, 'medecin/readSpeciality.html', context)

def readAllSpeciality(request):
    specialities = Speciality.objects.all()
    context = {
        'title': 'Ajouter Speciality',
        'specialities': specialities,
    }
    return render(request, 'medecin/readAllSpeciality.html', context)

@login_required
def updSpeciality(request, spc_name):
    speciality = Speciality.objects.get(title=spc_name)
    if request.method == 'PUT':
        nom = request.POST.get('nom', '')
        description = request.POST.get('description', '')

        speciality.nom = nom
        speciality.description = description
        speciality.save()
        return redirect('dashboard_m')
    context = {
        'title': 'Ajouter Speciality',
        'Speciality': speciality,
    }
    return render(request, 'medecin/updateSpeciality.html', context)

@login_required
def delSpeciality(request, spc_name):
    s = Hopital.objects.get(pk=spc_name)
    Archive.objects.create(content_object=s, archived_by=request.user)
    s.delete()
    return redirect('dashboard_m')

@user_passes_test(is_patient)
@login_required
def creaSante(request):
    if request.method == 'POST':
        patient = Patient.objects.get(pk=request.user.id)
        if (patient):
            CarnetSante.objects.create(patient=patient).save()
    return redirect('redirection')

@user_passes_test(is_patient)
@login_required
def readSante(request):
    carnet = get_object_or_404(CarnetSante, patient=request.user)
    context = {
        'title': 'Mon carnet de sante',
        'carnet': carnet,
    }
    return render(request, 'readSante.html', context)

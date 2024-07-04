from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import *

# create your views here.
# MEDECIN
@login_required
def dashboard(request):
    context = {
        'title': 'Medecin ' + request.user.user.username,
    }
    return render(request, 'dashboard.html', context)

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
    return render(request, 'createHospital.html', context)

def readHopital(request, hos_name):
    hospital = Hopital.objects.get(nom=hos_name)
    context = {
        'title': 'Afficher Hopital',
        'hopital': hospital,
    }
    return render(request, 'updateHospital.html', context)

def readAllHopital(request):
    hospitals = Hopital.objects.all()
    context = {
        'title': 'Afficher Hopitaux',
        'hopitals': hospitals,
    }
    return render(request, 'updateHospital.html', context)

@login_required
def updHopital(request, hos_name):
    hospital = Hopital.objects.get(nom=hos_name)
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
    return render(request, 'updateHospital.html', context)

@login_required
def delHopital(request, hos_name):
    if request.method == 'DEL':
        response = request.POST.get('response', '')
        if response == 'yes':
            Hopital.objects.get(nom=hos_name).delete()

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
    return render(request, 'createAdvice.html', context)

def readAdvice(request, adv_name):
    advice = Advice.objects.get(nom=adv_name)
    context = {
        'title': 'Ajouter Advice',
        'advice': advice,
    }
    return render(request, 'readAdvice.html', context)

def readAllAdvice(request):
    advice = Advice.objects.all()
    context = {
        'title': 'Afficher Advices',
        'advice': advice,
    }
    return render(request, 'readAllAdvice.html', context)

@login_required
def updAdvice(request, adv_name):
    advice = Advice.objects.get(nom=adv_name)
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
    return render(request, 'updateAdvice.html', context)

@login_required
def delAdvice(request, adv_name):
    if request.method == 'DEL':
        response = request.POST.get('response', '')
        if response == 'yes':
            Advice.objects.get(nom=adv_name).delete()

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
    return render(request, 'createConsigne.html', context)

def readConsigne(request, csg_name):
    consigne = Consigne.objects.get(nom=csg_name)
    context = {
        'title': 'Ajouter Consigne',
        'consigne': consigne,
    }
    return render(request, 'updateHospital.html', context)

def readAllConsigne(request):
    consignes = Consigne.objects.all()
    context = {
        'title': 'Afficher tous les Consignes',
        'consignes': consignes,
    }
    return render(request, 'readAllConsigne.html', context)

@login_required
def updConsigne(request, csg_name):
    consigne = Consigne.objects.get(nom=csg_name)
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
    return render(request, 'updateHospital.html', context)

@login_required
def delConsigne(request, csg_name):
    if request.method == 'DEL':
        response = request.POST.get('response', '')
        if response == 'yes':
            Consigne.objects.get(nom=csg_name).delete()

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
    return render(request, 'createPrescription.html', context)

def readPrescription(request, prsc_title):
    prescription = Prescription.objects.get(nom=prsc_title)
    context = {
        'title': 'Afficher Prescription',
        'Prescription': prescription,
    }
    return render(request, 'readPrscription.html', context)

def readAllPrescription(request):
    prescriptions = Prescription.objects.all()
    context = {
        'title': 'Afficher Les Prescriptions',
        'prescriptions': prescriptions,
    }
    return render(request, 'readAllPrscription.html', context)

@login_required
def updPrescription(request, prsc_title):
    prescription = Prescription.objects.get(nom=prsc_title)
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
    return render(request, 'updatePrescription.html', context)

@login_required
def delPrescription(request, prsc_title):
    if request.method == 'DEL':
        response = request.POST.get('response', '')
        if response == 'yes':
            Prescription.objects.get(nom=prsc_title).delete()

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
    return render(request, 'createSpeciality.html', context)

def readSpeciality(request, spc_name):
    speciality = Speciality.objects.get(title=spc_name)
    context = {
        'title': 'Ajouter Speciality',
        'Speciality': speciality,
    }
    return render(request, 'readSpeciality.html', context)

def readAllSpeciality(request):
    specialities = Speciality.objects.all()
    context = {
        'title': 'Ajouter Speciality',
        'specialities': specialities,
    }
    return render(request, 'readAllSpeciality.html', context)

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
    return render(request, 'updateSpeciality.html', context)

@login_required
def delSpeciality(request, spc_name):
    if request.method == 'DEL':
        response = request.POST.get('response', '')
        if response == 'yes':
            Speciality.objects.get(title=spc_name).delete()

"""
    Sub Speciality CRUD
"""
@login_required
def creaSubSpeciality(request):
    if request.method == 'POST':
        nom = request.POST.get('nom', '')
        description = request.POST.get('description', '')

        SubSpeciality.objects.create(nom=nom, description=description).save()
        return redirect('dashboard_m')
    context = {
        'title': 'Ajouter SubSpeciality',
    }
    return render(request, 'createSubSpeciality.html', context)

def readSubSpeciality(request, subSpc_name):
    subSpeciality = SubSpeciality.objects.get(nom=subSpc_name)
    context = {
        'title': 'Ajouter SubSpeciality',
        'SubSpeciality': subSpeciality,
    }
    return render(request, 'updateSubSpeciality.html', context)

def readAllSubSpeciality(request):
    subSpecialities = SubSpeciality.objects.all()
    context = {
        'title': 'Ajouter SubSpeciality',
        'subSpecialities': subSpecialities,
    }
    return render(request, 'readAllSubSpeciality.html', context)

@login_required
def updSubSpeciality(request, subSpc_name):
    subSpeciality = SubSpeciality.objects.get(nom=subSpc_name)
    if request.method == 'PUT':
        nom = request.POST.get('nom', '')
        description = request.POST.get('description', '')

        subSpeciality.nom = nom
        subSpeciality.description = description
        subSpeciality.save()
        return redirect('dashboard_m')
    context = {
        'title': 'Modifier SubSpeciality',
        'SubSpeciality': subSpeciality,
    }
    return render(request, 'updSubSpeciality.html', context)

@login_required
def delSubSpeciality(request, subSpc_name):
    if request.method == 'DEL':
        response = request.POST.get('response', '')
        if response == 'yes':
            SubSpeciality.objects.get(nom=subSpc_name).delete()


from datetime import datetime
from django.http import Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test

from pharmacie.views import is_patient, is_doctor
from .models import *

# create your views here.
# MEDECIN
@login_required
def dashboard(request):
    medecin = get_object_or_404(Medecin, id=request.user.id)
    rdvs = Appointement.objects.filter(medecin=medecin, is_send=False, status='EN ATTENTE').all()
    rdva = Appointement.objects.filter(medecin=medecin, is_send=False, status='ACCEPTÉ').all()
    context = {
        'title': 'Medecin ' + medecin.username,
        'rdvs': rdvs,
        'rdva': rdva, 'm': medecin,
        's': len(rdvs),
        'a': len(rdva),
        'date': medecin.date_joined.strftime('%b %Y'),
    }
    return render(request, 'medecin/dashboard.html', context)

@login_required
def refuse(request, id):
    rdv = get_object_or_404(Appointement, pk=id)
    rdv.status = rdv.STATUS_CHOICE[1][1]  # Set status to "accepté"
    rdv.save()
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
    m = get_object_or_404(Medecin, pk=request.usrer.id)
    if request.method == 'POST':
        nom = request.POST.get('nom', '')
        adresse = request.POST.get('adresse', '')
        localisation = request.POST.get('localisation', '')
    
        h = Hopital.objects.create(nom=nom, adresse=adresse, localisation=localisation)
        h.medecins.add(m)
        h.save()
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

def myHopital(request):
    m = get_object_or_404(Medecin, pk=request.user.id)
    hospital = Hopital.objects.get(hopitaux=m).first()
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
@user_passes_test(is_doctor)
@login_required
def creaAdvice(request):
    user = get_object_or_404(Medecin, pk=request.user.id)
    ills = Maladie.objects.all()
    if request.method == 'POST':
        title = request.POST.get('title', '')
        content = request.POST.get('content', '')
        ill = request.POST.get('ill', '')
        image = request.FILES.get('image', '')

        Advice.objects.create(title=title, content=content, ill=ill, image=image, medecin=user).save()
        return redirect('readMy_adv')
    context = {
        'title': 'Ajouter Conseil',
        'illness': ills,
    }
    return render(request, 'medecin/createAdvice.html', context)

def readAdvice(request, id):
    advice = Advice.objects.get(pk=id)
    context = {
        'title': 'Ajouter Conseil',
        'advice': advice,
    }
    return render(request, 'medecin/readAdvice.html', context)

def readAllAdvice(request):
    advice = Advice.objects.all()
    base = "base.html"
    context = {
        'title': 'Afficher Conseils',
        'advices': advice,
        'base': base,
    }
    return render(request, 'medecin/readAllAdvice.html', context)

@user_passes_test(is_doctor)
@login_required
def readMyAdvice(request):
    user = get_object_or_404(Medecin, pk=request.user.id)
    advice = Advice.objects.filter(medecin=user).all()
    context = {
        'title': 'Afficher Conseils',
        'advice': advice,
    }
    return render(request, 'medecin/readMyAdvice.html', context)

@user_passes_test(is_doctor)
@login_required
def updAdvice(request, id):
    advice = Advice.objects.get(pk=id)
    ills = Maladie.objects.all()
    if request.method == 'PUT':
        title = request.POST.get('title', '')
        content = request.POST.get('content', '')
        ill = request.POST.get('ill', '')
        image = request.FILES.get('image', '')

        advice.title, advice.content, advice.ill, advice.image = title, content, ill, image
        advice.save()
        return redirect('readMy_adv')
    context = {
        'title': 'Modifier Conseil',
        'advice': advice,
        'illness': ills,
    }
    return render(request, 'medecin/updateAdvice.html', context)

@login_required
def delAdvice(request, id):
    a = Advice.objects.get(pk=id)
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
def creaPrescription(request, p_id, c_id):
    med = Medication.objects.all()
    if request.method == 'POST':
        title = request.POST.get('title', '')
        # consigne = request.POST.get('consigne', None)
        med = request.POST.get('medication', None)
        patient = get_object_or_404(Patient, pk=p_id)
        m = get_object_or_404(Medecin, pk=request.user.id)
        consultation = get_object_or_404(Consultation, pk=c_id)

        p = Prescription.objects.create(title=title, medecin=m, patient=patient, consultation=consultation)
        # p.consigne.add(consigne)
        if med:
            p.medications.add(med)
        p.save()
        return redirect('dashboard_m')
    context = {
        'title': 'Ajouter Prescription',
        'medications': med,
        'id': p_id, 'cons': c_id,
    }
    return render(request, 'medecin/createPrescription.html', context)

def readPrescription(request, id):
    prescription = Prescription.objects.get(pk=id)
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

"""
    Carnet de Sante CRUD
"""
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
    patient = Patient.objects.get(pk=request.user.id)
    carnet = get_object_or_404(CarnetSante, patient=patient)
    context = {
        'title': 'Mon carnet de sante',
        'carnet': carnet,
    }
    return render(request, 'readSante.html', context)

"""
    Consultation CRUD
"""
@user_passes_test(is_doctor)
@login_required
def creaConsultation(request, p_id, title):
    p = get_object_or_404(Patient, pk=p_id)
    medecin = get_object_or_404(Medecin, pk=request.user.id)
    cS = CarnetSante.objects.get(patient=p)
    if request.method == 'POST':
        motif = request.POST.get('motif', '')
        diagnostic = request.POST.get('diagnostic', '')
        poids = request.POST.get('poids', 0)
        taille = request.POST.get('taille', 0)
        price = request.POST.get('price', 0)
        temperature = request.POST.get('temperature', '')
        tension_arterielle = request.POST.get('tension_arterielle', '')
        frequence_cardiaque = request.POST.get('frequence_cardiaque', '')
        notes = request.POST.get('notes', '')
        try:
            rdv = get_object_or_404(Appointement, patient=p, medecin=medecin)
        except Appointement.DoesNotExist:
            rdv = None
            raise Http404("Rendez-vous non trouvé")
        except Appointement.MultipleObjectsReturned:
            rdv = Appointement.objects.get(patient=p, medecin=medecin).last()

        c = Consultation.objects.create(
            motif=motif,
            diagnostic=diagnostic,
            poids=poids,
            taille=taille,
            medecin=medecin,
            typeConsult="Analyse Generale",
            price=price,
            rdv=rdv,
            temperature=temperature,
            tension_arterielle=tension_arterielle,
            frequence_cardiaque=frequence_cardiaque,
            notes=notes
        )
        c.save()
        h = Hospitalisation.objects.create(patient=p, title=title, date_admission=datetime.now(), consultation=c)
        h.save()
        cS.add_hosp(h)
        return redirect('create_prsc', p_id, c.id)
    context = {
        'title': 'cree une consultation',
        'title': title,
        'id': p_id,
    }
    return render(request, 'medecin/creaconsult.html', context)

@login_required
def readConsult(request, c_id):
    user = get_object_or_404(Medecin, pk=request.user.id)
    consult = get_object_or_404(Consultation, pk=c_id)

    context ={
        'title': 'Consultation',
        'consultation': consult,
    }
    return render(request, 'medecin/consultation.html', context)

def delConsultation(request, id):
    s = Consultation.objects.get(pk=id)
    a = Archive.objects.create(content_object=s.id, archived_by=request.user.id)
    a.save()
    s.delete()
    return redirect('dashboard_m')

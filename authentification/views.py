from django.contrib.sessions.models import Session
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.utils import timezone
from .models import *

# Create your views here.
def dash(user):
    if isinstance(user, Patient):
        return redirect('dashboard_p')
    elif isinstance(user, Medecin):
        return redirect('dashboard_m')
    elif isinstance(user, Pharmacien):
        return redirect('dashboard_ph')

@login_required
def redirection(request):
    user = None
    try:
        user = Patient.objects.get(first_name=request.user.first_name)
    except Patient.DoesNotExist:
        try:
            user = Medecin.objects.get(first_name=request.user.first_name)
        except Medecin.DoesNotExist:
            try:
                user = Pharmacien.objects.get(first_name=request.user.first_name)
            except Pharmacien.DoesNotExist:
                pass
    if user is not None:
        dash(user)
    else: return redirect('home')

def log_in(request):
    if request.method == 'POST':
        email = request.POST.get('email', '')
        password = request.POST.get('password', '')

        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            dash(user)

@login_required
def out(request):
    logout(request)
    return redirect('home')

def log_on_patient(request):
    if request.method == "POST":
        firstname = request.POST.get('firstname', '')
        lastname = request.POST.get('lastname', '')
        username = request.POST.get('username', '')
        email = request.POST.get('email', '')
        password = request.POST.get('password', '')

        mobile = request.POST.get('mobile', '')
        sexe = request.POST.get('sexe', '')
        profession = request.POST.get('profession', '')

        patient = Patient.objects.create(mobile=mobile, profession=profession, sexe=sexe, firstname=firstname, lastname=lastname, username=username, email=email, password=password)
        patient.save()
        send_mail(
            'INSCRIPTION SUR HEALTH',
            'Felicition, vous venez de creer un compte sur notre plateforme. Merci de votre fidelite',
            'healthy@health@gmail.com', 
            [email]
        )
        return redirect('log')

def log_on_sante(request):
    if request.method == "POST":
        status = request.POST.get('status', '')

        firstname = request.POST.get('firstname', '')
        lastname = request.POST.get('lastname', '')
        username = request.POST.get('username', '')
        email = request.POST.get('email', '')
        password = request.POST.get('password', '')

        mobile = request.POST.get('mobile', '')
        sexe = request.POST.get('sexe', '')
        preuve = request.POST.get('preuve', '')

        if status == 'medecin':
            medoc = Medecin.objects.create(mobile=mobile, preuveMedecin=preuve, sexe=sexe, firstname=firstname, lastname=lastname, username=username, email=email, password=password, preuve=preuve)
            medoc.save()
            send_mail(
                'INSCRIPTION SUR HEALTH',
                'Felicition, vous venez de creer un compte Medecin sur notre plateforme. Merci de votre fidelite.\nNous aurons a verifie votre document fourni et nous vous revenons tres bientot.',
                'healthy@health@gmail.com', 
                [email]
            )
        elif status == 'pharmacien':
            pharm = Pharmacien.objects.create(mobile=mobile, preuvePharmacien=preuve, sexe=sexe, firstname=firstname, lastname=lastname, username=username, email=email, password=password, preuve=preuve)
            pharm.save()
            send_mail(
                'INSCRIPTION SUR HEALTH',
                'Felicition, vous venez de creer un compte Pharmacien sur notre plateforme. Merci de votre fidelite.\nNous aurons a verifie votre document fourni et nous vous revenons tres bientot.',
                'healthy@health@gmail.com', 
                [email]
            )
        return redirect('home')

def auth(request):
    context = {
        'title': 'Authentification',
    }
    return render(request, 'auth/auth.html', context)

def auth_sante(request):
    context = {
        'title': 'Authentification de personnel',
    }
    return render(request, 'auth/auth_hos.html', context)

@login_required
def deleteAccount(request):
    if request.method == "POST":
        response = request.POST.get('response', '')
        user = request.user
        if response == 'yes':
            Archive.objects.create(content_object=user, archived_by=user).save()
            if user:
                user.delete()
                out()

@login_required
def lock(request):
    if request.method == "POST":
        password = request.POST.get('password', '')
        user = authenticate(request, email=request.user.email, password=password)
        if user is not None:
            login(request, user)
            dash(user)

@login_required
def veille(request):
    context = {
        'title': 'Page de Veille',
    }
    return render(request, 'auth/lockscreen.html', context)

@login_required
def check_user_activity():
    active_sessions = Session.objects.filter(expire_date__gte=timezone.now()) # Récupérer toutes les sessions actives

    for session in active_sessions: # Parcourir les sessions actives
        session_data = session.get_decoded()
        user_id = session_data.get('_auth_user_id')

        if user_id is not None and (timezone.now() - session.last_activity).seconds > 10800: # Vérifier si l'utilisateur est connecté et si la durée d'inactivité est supérieure à 3 heure
            logout(session.session_key)  # Déconnexion de l'utilisateur au bout d'3h d'inactivite
        if user_id is not None and (timezone.now() - session.last_activity).seconds > 3600: # Vérifier si l'utilisateur est connecté et si la durée d'inactivité est supérieure à 1 heure
            return redirect('veille')

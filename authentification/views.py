from django.contrib.sessions.models import Session
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
# from django.core.mail import send_mail
from django.utils import timezone
from .models import *

# Create your views here.
def dash(request):
    if request.user.is_authenticated:
        user = request.user
        if hasattr(user, 'medecin'):
            return redirect('dashboard_m')
        elif hasattr(user, 'pharmacien'):
            return redirect('dashboard_ph')
    return redirect('dashboard_p')

def redirection(request):
    user = None
    if request.user.is_authenticated:
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
            dash(request)
    return redirect('home')

def log_in(request):
    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return dash(request)
        else:
            return render(request, 'auth/auth.html', {'error': 'Identifiants invalides'})
    return redirect('log')

@login_required
def out(request):
    logout(request)
    return redirect('home')

def log_on_patient(request):
    if request.method == "POST":
        username = request.POST.get('username', '')
        email = request.POST.get('email', '')
        password = request.POST.get('password', '')
        password = make_password(password)

        patient = Patient.objects.create(email=email, username=username, password=password)
        patient.save()
        """ send_mail(
            'INSCRIPTION SUR HEALTH',
            'Felicition, vous venez de creer un compte sur notre plateforme. Merci de votre fidelite',
            'healthy@health@gmail.com', 
            [email]
        ) """
    return redirect('log')

def log_on_sante(request):
    if request.method == "POST":
        status = request.POST.get('status', '')

        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        password = make_password(password)

        if status == 'medecin':
            medoc = Medecin.objects.create(username=username, password=password)
            medoc.save()
        elif status == 'pharmacien':
            pharm = Pharmacien.objects.create(username=username, password=password)
            pharm.save()
        return redirect('check_status', username, status)
    return redirect('log')

def check_status(request, username, status):
    user = None
    if request.method == 'POST':
        sexe = request.POST.get('sexe', '')
        last_name = request.POST.get('last_name', '')
        first_name = request.POST.get('first_name', '')
        mobile = request.POST.get('mobile', '')
        preuve = request.FILES.get('preuve', None)

        if  status == 'medecin':
            user = Medecin.objects.get(username=username)
        elif status == 'pharmacien':
            user = Pharmacien.objects.get(username=username)

        if user is not None:
            user.sexe = sexe
            user.last_name = last_name
            user.first_name = first_name
            user.mobile = mobile
            user.preuve = preuve
            user.save()
            return redirect('home')
        return redirect('log_hos')
    context = {
        'title': 'Verification du status',
        'username': username,
        'status': status,
    }
    return render(request, 'auth/check.html', context)

def auth(request):
    context = {
        'title': 'Verification du status',
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
            dash(request)

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

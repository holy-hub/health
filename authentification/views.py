from django.contrib.sessions.models import Session
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect, get_object_or_404
# from django.core.mail import send_mail
from django.utils import timezone
from .models import *

# Create your views here.
def dash(request):
    user = get_object_or_404(Utilisateur, pk=request.user.id)
    if user.is_medecin:
        return redirect('dashboard_m')
    elif user.is_pharmacien:
        return redirect('dashboard_ph')
    elif user.is_patient:
        return redirect('dashboard_p')
    else:
        return redirect('home')

def redirection(request):
    if request.user.is_authenticated:
        return dash(request)
    else:
        return redirect('home')

def log_in(request):
    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')

        utilisateur = authenticate(request, username=username, password=password)
        if utilisateur is not None:
            user = get_object_or_404(Utilisateur, id=utilisateur.id)
            login(request, user)
            if user.is_medecin:
                return redirect('dashboard_m')
            elif user.is_pharmacien:
                return redirect('dashboard_ph')
            else:
                return redirect('dashboard_p')
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
        else:
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
            user = get_object_or_404(Medecin, username=username)
        elif status == 'pharmacien':
            user = get_object_or_404(Pharmacien, username=username)

        if user is not None:
            user.sexe = sexe
            user.last_name = last_name
            user.first_name = first_name
            user.mobile = mobile
            user.preuve = preuve
            user.save()
            message = "Vous receivrez un message dans les jour a venir, le temps d'examiner votre document."
            if message:
                request.session['message'] = message # Transmettez le message à la page 'home' via la session
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

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.core.mail import send_mail
from .models import *

# Create your views here.
def login(request):
    if request.method == 'POST':
        email = request.POST.get('email', '')
        password = request.POST.get('password', '')

        user = authenticate(email=email, password=password)
        if user is not None:
            user = User.objects.get(email='email')
            user = Utilisateur.objects.get(user=user)
            if user.deleted:
                return redirect("home")
            else:
                login(request, user)
                if user.status == "medecin": return redirect('dashboard_m')
                elif user.status == "pharmacien": return redirect('dashboard_ph')
                else: return redirect('dashboard_p')

@login_required
def out(request):
    logout(request)
    return redirect('home')

def register(request):
    if request.method == "POST":
        firstname = request.POST.get('firstname', '')
        lastname  = request.POST.get('lastname', '')
        username  = request.POST.get('username', '')
        email     = request.POST.get('email', '')
        password  = request.POST.get('password', '')

        mobile = request.POST.get('mobile', '')
        status = request.POST.get('status', '')
        preuve = request.POST.get('preuve', '')

        user = User.objects.create(firstname=firstname, lastname=lastname, username=username, email=email, password=password)
        utilisateur = Utilisateur.objects.create(user=user, mobile=mobile, status=status, preuve=preuve)
        user.save()
        utilisateur.save()
        send_mail(
            'INSCRIPTION SUR HEALTH',
            'Felicition, vous venez de creer un compte sur notre plateforme. Merci de votre fidelite',
            'healthy@health@gmail.com', 
            [email]
        )
        return redirect('log')

@login_required
def auth(request):
    context = {
        'title': 'Authentification',
    }
    return render(request, 'register.html', context)

@login_required
def deleteAccount(request):
    if request.method == "POST":
        response = request.POST.get('response', '')
        user     = request.user
        if response == 'yes':
            Archive.objects.create(content_object=user, archived_by=user).save()
            if user:
                user.delete()
                return redirect('home')
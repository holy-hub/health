from django.test import TestCase
from authentification.models import Utilisateur, Patient, Medecin, Pharmacien
# Create your tests here.
def test():
    u1 = Utilisateur.objects.create(username="nom1", first_name="Nom1", last_name="Prenom1", mobile="1234567890", address="Adresse 1")
    u2 = Utilisateur.objects.create(username="nom2", first_name="Nom2", last_name="Prenom2", mobile="1234567891", address="Adresse 2")
    u3 = Utilisateur.objects.create(username="nom3", first_name="Nom3", last_name="Prenom3", mobile="1234567892", address="Adresse 3")
    
    p = Patient.objects.create(
        username=u1.username, 
        first_name=u1.first_name, 
        last_name=u1.last_name, 
        mobile=u1.mobile, 
        address=u1.address, 
        assurance_medicale=True, 
        code_assurance="XYZ123", 
        personne_a_prevenir="John Doe", 
        tel_personne_a_prevenir="0987654321"
    )
    
    m = Medecin.objects.create(
        username=u2.username, 
        first_name=u2.first_name, 
        last_name=u2.last_name, 
        mobile=u2.mobile, 
        address=u2.address, 
        preuveMedecin="document.pdf"
    )
    
    ph = Pharmacien.objects.create(
        username=u3.username, 
        first_name=u3.first_name, 
        last_name=u3.last_name, 
        mobile=u3.mobile, 
        address=u3.address, 
        preuvePharmacien="attestation.pdf"
    )
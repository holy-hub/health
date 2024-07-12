from authentification.models import Archive, Medecin, Patient
from django.db.models import ProtectedError
from pharmacie.models import *
from patient.models import Appointement
from django.db import models

# Create your models here.
class Hopital(models.Model):
    nom = models.CharField(max_length=50)
    adresse = models.CharField(max_length=50, unique=True)
    localisation = models.URLField(max_length=255)
    medecins = models.ManyToManyField(Medecin, verbose_name="Medecin de l'hôpital", related_name="hopitaux")

    def __str__(self):
        return f"{self.nom} situe a l'adresse {self.adresse}."

    def add_medecin(self, user):
        if user.is_medecin:
            self.medecins.add(user)
    
    def delete_medcin(self, id):
        """
        Utilisé lors d'un licenciement ou un depart d'un médecin 
        """
        user = Medecin.objects.get(pk=id)
        if  user in self.medecins:
            self.medecins.remove(user)

    def get_medecins(self):
        return [str(medecin) for medecin in self.medecins]

class Advice(models.Model):
    title = models.CharField(max_length=150, verbose_name="Titre du conseil")
    content = models.TextField(verbose_name="Contenu du conseil")
    ill = models.OneToOneField(Maladie, verbose_name="Maladie choisie pour le conseil", on_delete=models.CASCADE)
    medecin = models.ForeignKey(Medecin, verbose_name="Medecin originaire de cette enregistrement", on_delete=models.CASCADE)
    image = models.FileField(upload_to="image/conseils/", max_length=255)
    is_publish = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Intitulé {self.title} portant sur la maladie {self.ill}."

    def publish(self):
        self.is_publish = True
        return self.is_publish
    
    def archive(self):
        Archive.objects.create(content_object=self, archived_by=self.medecin).save()
        self.is_publish = False
        return self.is_publish

class Consigne(models.Model):
    POSOLOGIE_CHOICE = (
        ('comprimé 0.5', 'Moitié de comprimé par jour'),
        ('comprimé 1', '1 comprimé par jour'),
        ('comprimé 2', '2 comprimés par jour'),
        ('comprimé 3', '3 comprimés par jour'),
        ('sirop 1', '1 cuillerée par jour'),
        ('sirop 2', '2 cuillerées par jour'),
        ('sirop 3', '3 cuillerées par jour'),
        ('poudre 1', '1 sachet par jour'),
        ('poudre 2', '2 sachets par jour'),
        ('poudre 3', '3 sachets par jour'),
    )
    medication = models.ForeignKey(Medication, verbose_name="Les medicaments prescrits", null=True, on_delete=models.CASCADE)
    posologie = models.CharField(max_length=50, choices=POSOLOGIE_CHOICE, null=True)

    def __str__(self):
        return f"{self.medication.nom} suit la posologie `{self.posologie}`."

class Prescription(models.Model):
    title = models.CharField(max_length=50)
    temperature = models.PositiveSmallIntegerField(default=37)
    observation = models.TextField(verbose_name="Observations du medecin")
    consigne = models.ManyToManyField(Consigne, verbose_name="Les medications et leur posologie a suivre")
    patient = models.ForeignKey(Patient, related_name='prescriptions_patient', verbose_name="Patient de consultation", on_delete=models.CASCADE)
    medecin = models.ForeignKey(Medecin, related_name='prescriptions_medecin', verbose_name="Medecin de consultation", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.medecin.username} prescrit cette ordonnance au patient #{self.patient.user.username} ayant une temperature de {self.temperature}*C."

    def save(self, *args, **kwargs):
        if self.medecin.is_medecin and self.patient.is_patient:
            super().save(*args, **kwargs)

    def get_consignes(self):
        return [str(consigne) for consigne in self.consigne.all()]

class Speciality(models.Model):
    nom = models.CharField(max_length=50, unique=True)
    description = models.TextField(verbose_name="description de la Spécialité")

    def __str__(self):
        return f"Specialite: {self.nom}."

    def delete(self, *args, **kwargs):
        if self.subspeciality_set.exists():
            raise ProtectedError("Impossible de supprimer cette modalité car elle est utilisée dans une ou plusieurs modalité(s).", self)
        super().delete(*args, **kwargs)

class Service(models.Model):
    nom = models.CharField(max_length=50)
    medecin = models.ForeignKey(Medecin, verbose_name="", on_delete=models.CASCADE)

class Chambre(models.Model):
    capacity = models.IntegerField()
    price = models.FloatField()
    service = models.ForeignKey(Service, verbose_name="", on_delete=models.CASCADE)

class Traitement(models.Model):
    date_traitement = models.DateTimeField()
    price = models.FloatField()
    chambre = models.ForeignKey(Chambre, verbose_name="", on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Traitement"
        verbose_name_plural = "Traitements"

    def save(self, *args, **kwargs):
        if self.chambre.service == self.medecin.service:
            super().save(*args, **kwargs)

    def price_total(self):
        price = self.price + self.chambre.price
        return price

class ExamenBiologique(Traitement):
    designation = models.CharField(max_length=250)
    resultat_examen = models.TextField()
    image = models.ImageField(upload_to='health/radiology/')

class Chirurgie(Traitement):
    chirurgien = models.CharField(max_length=50)
    anesthesiste = models.CharField(max_length=50)

class Facture(models.Model):
    date = models.DateTimeField(auto_now_add=True)
    prix_total = models.FloatField(default=0)

    def get_prixTotal(self):
        return self.hospitalisation.getPrice()

class Hospitalisation(models.Model):
    date_admission = models.DateTimeField()
    motif_admission = models.TextField()
    accompagnant = models.CharField(max_length=50)
    tel_accompagnant = models.CharField(max_length=50)
    date_entree = models.DateTimeField(auto_now_add=True)
    date_sortie = models.DateTimeField()
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    resultats = models.CharField(max_length=255)
    date_resultats = models.DateTimeField()
    traitements = models.ManyToManyField(Traitement, verbose_name="")
    nom_deces = models.CharField(max_length=50)
    date_deces = models.DateTimeField()
    facture = models.ForeignKey(Facture, on_delete=models.CASCADE)

    def getPrice(self):
        for traitement in self.traitements:
            self.facture.prix_total += traitement.price_total()
        return self.facture.prix_total

class CarnetSante(models.Model):
    poids = models.FloatField()
    taille = models.FloatField()
    temperature = models.FloatField()
    tension_arterielle = models.CharField(max_length=20)
    frequence_cardiaque = models.IntegerField()
    notes = models.TextField()
    hospitalisation = models.ForeignKey(Hospitalisation, related_name='facture_patient', on_delete=models.CASCADE)
    date_creation = models.DateTimeField(auto_now_add=True)
    date_modification = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Carnet de santé de {self.patient.user.username} suivi par {self.medecin.user.username}."

    def get_carnet_sante_medecin(self):
        return CarnetSante.objects.filter(medecin=self.hospitalisation.medecin).all()

    def get_carnet_sante_patient(self):
        return CarnetSante.objects.filter(patient=self.hospitalisation.patient).all()

class Consultation(models.Model):
    medecin = models.ForeignKey(Medecin, related_name='consultations_medecin', on_delete=models.CASCADE)
    patient = models.ForeignKey(Patient, related_name='consultations_patient', on_delete=models.CASCADE)
    date_consultation = models.DateTimeField()
    motif = models.TextField()
    diagnostic = models.TextField()
    rdv = models.ForeignKey(Appointement, verbose_name="", on_delete=models.CASCADE)
    typeConsult = models.CharField(max_length=50)
    price = models.FloatField()
    date_creation = models.DateTimeField(auto_now_add=True)
    date_modification = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Consultation du {self.date_consultation} pour {self.patient.user.username} par {self.medecin.user.username}"

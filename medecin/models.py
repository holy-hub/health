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
        if isinstance(user, Medecin):
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
    image = models.FileField(upload_to="Medecin/conseils/", max_length=255)
    is_publish = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Intitulé {self.title} portant sur la maladie {self.ill.nom}."

    def publish(self):
        self.is_publish = True
        return self.is_publish

    def retirer(self):
        if self.is_publish:
            self.is_publish = False
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
    prixTotal = models.FloatField(blank=True, default=0)

    class Meta:
        verbose_name = "Traitement"
        verbose_name_plural = "Traitements"

    def price_total(self):
        self.prixTotal = self.price + self.chambre.price
        return self.prixTotal

class ExamenBiologique(Traitement):
    designation = models.CharField(max_length=250)
    resultat_examen = models.TextField()
    image = models.ImageField(upload_to='Medecin/radiology/')

class Chirurgie(Traitement):
    chirurgien = models.CharField(max_length=50)
    anesthesiste = models.CharField(max_length=50)

class Consultation(models.Model):
    medecin = models.ForeignKey(Medecin, related_name='consultation_medecin', on_delete=models.CASCADE)
    date_consultation = models.DateTimeField(auto_now_add=True)
    motif = models.TextField()
    diagnostic = models.TextField()
    poids = models.FloatField( default=0,)
    taille = models.FloatField( default=1.0,)
    rdv = models.ForeignKey(Appointement, verbose_name="", on_delete=models.CASCADE)
    typeConsult = models.CharField(max_length=50)
    price = models.FloatField(default=0)
    temperature = models.FloatField(default=37)
    tension_arterielle = models.CharField(max_length=20, default=0)
    frequence_cardiaque = models.IntegerField(default=0)
    notes = models.TextField(blank=True)
    date_modification = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Consultation du {self.date_consultation} pour {self.patient.username} par {self.medecin.username}"

class Prescription(models.Model):
    title = models.CharField(max_length=50)
    consigne = models.ManyToManyField(Consigne, verbose_name="Les medications et leur posologie a suivre", blank=True)
    patient = models.ForeignKey(Patient, related_name='prescriptions_patient', verbose_name="Patient de consultation", on_delete=models.CASCADE)
    medecin = models.ForeignKey(Medecin, related_name='prescriptions_medecin', verbose_name="Medecin de consultation", on_delete=models.CASCADE)
    consultation = models.ForeignKey(Consultation, related_name='consultation_medecin', blank=True, verbose_name="consultation du Medecin", default=None, on_delete=models.CASCADE)
    medications = models.ManyToManyField(Medication, verbose_name="medicaments de prescription", blank=True, default=None)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.medecin.username} prescrit cette ordonnance au patient #{self.patient.username} ayant une temperature de {self.temperature}*C."

    def save(self, *args, **kwargs):
        if self.medecin.is_medecin and self.patient.is_patient:
            super().save(*args, **kwargs)

    def get_consignes(self):
        return [str(consigne) for consigne in self.consigne.all()]

    def get_medications(self):
        return [str(medication) for medication in self.medications.all()]

class Hospitalisation(models.Model):
    title = models.CharField(max_length=50, default="Facture")
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    consultation = models.ForeignKey(Consultation, default=None, blank=True, on_delete=models.CASCADE)
    traitements = models.ManyToManyField(Traitement, verbose_name="", blank=True, default=None)
    date_admission = models.DateTimeField()
    motif_admission = models.TextField()
    date_entree = models.DateTimeField(auto_now_add=True)
    date_resultats = models.DateTimeField(auto_now=True)
    resultats = models.CharField(max_length=255)

    def __str__(self):
        return self.title

class Facture(models.Model):
    patient = models.ForeignKey(Patient, verbose_name="Facture du patient", default=None, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    prix_total = models.FloatField(default=0)
    hospitalisation = models.ForeignKey(Hospitalisation, default=None, on_delete=models.CASCADE)


    def getPrice(self):
        for traitement in self.hospitalisation.traitements:
            self.prix_total += traitement.priceTotal()
        self.prix_total += self.hospitalisation.consultation.price
        return self.prix_total

    def historique(self):
        traitement_total = sum(traitement.priceTotal() for traitement in self.hospitalisation.traitements)
        consultation_price = self.hospitalisation.consultation.price
        total_price = traitement_total + consultation_price

        return f"""
            - {'Consultation':20} : {consultation_price:8} F CFA
            - {'Prix des traitements':20} : {traitement_total:8} F CFA
            ---------------------------------------
            - {'Prix Total':20} : {total_price:8} F CFA
        """

class CarnetSante(models.Model):
    patient = models.OneToOneField(Patient, related_name="patient_carnet", default=None, verbose_name="Carnet_patient", on_delete=models.CASCADE)
    hospitalisations = models.ManyToManyField(Hospitalisation, related_name='hospitalisation_patient_carnetSante')
    date_creation = models.DateTimeField(auto_now_add=True)
    date_modification = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Carnet de santé de {self.patient.last_name} cre le {self.date_creation.strftime('%b %Y, %A %d')}."

    def add_hosp(self, hospitalisation):
        if isinstance(hospitalisation, Hospitalisation):
            self.hospitalisations.add(hospitalisation)

from django.contrib.auth.models import User
from authentification.models import *
from django.db.models import ProtectedError
from pharmacie.models import *
from django.db import models

# Create your models here.
class Advice(models.Model):
    title = models.CharField(max_length=150, verbose_name="Titre du conseil")
    content = models.TextField(verbose_name="Contenu du conseil")
    ill = models.OneToOneField(Maladie, verbose_name="Maladie choisie pour le conseil", on_delete=models.CASCADE)
    medecin = models.ForeignKey(User, verbose_name="Medecin originaire de cette enregistrement", on_delete=models.CASCADE)
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
    patient = models.ForeignKey('authentification.Utilisateur', related_name='prescriptions_patient', verbose_name="Patient de consultation", on_delete=models.CASCADE)
    medecin = models.ForeignKey('authentification.Utilisateur', related_name='prescriptions_medecin', verbose_name="Medecin de consultation", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.medecin.user.username} prescrit cette ordonnance au patient #{self.patient.user.username} ayant une temperature de {self.temperature}*C."
    
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

class SubSpeciality(models.Model):
    nom = models.CharField(max_length=50, unique=True)
    description = models.TextField(verbose_name="description de la Spécialité")
    speciality = models.ForeignKey(Speciality, verbose_name="Specialite de cette sous spécialité", on_delete=models.CASCADE)

    def __str__(self):
        return f"Sous specialite #{self.nom} est branche de {self.speciality.nom}."

class Hopital(models.Model):
    nom = models.CharField(max_length=50)
    adresse = models.CharField(max_length=50, unique=True)
    localisation = models.URLField(max_length=255)
    medecins = models.ManyToManyField('authentification.Utilisateur', verbose_name="Medecin de l'hôpital", related_name="hopitaux")

    def __str__(self):
        return f"{self.nom} situe a l'adresse {self.adresse}."

    def add_medecin(self, user):
        if user.is_medecin:
            self.medecins.add(user)
    
    def delete_medcin(self, id):
        """
        Utilisé lors d'un licenciement ou un depart d'un médecin 
        """
        user = 'authentification.Utilisateur'.objects.get(pk=id)
        if  user in self.medecins:
            self.medecins.remove(user)

    def get_medecins(self):
        return [str(medecin) for medecin in self.medecins]


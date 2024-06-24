from django.db               import models
from authentification.models import *

# Create your models here.
class Medication(models.Model):
    nom  = models.CharField(max_length=250)
    role = models.TextField(verbose_name="Les effets de ce medicament.")
    prix = models.PositiveIntegerField(default=0)
    
    def __init__(self):
        return f"{self.nom} à {self.prix} F CFA."

class Pharmacie(models.Model):
    nom         = models.CharField(max_length=250, verbose_name="Nom de la pharmacie.")
    description = models.TextField(verbose_name="Situer la pharmacie")
    location    = models.URLField(max_length=200, verbose_name="Coordonnées de la pharmacie.")
    pharmacien  = models.ForeignKey(Utilisateur, verbose_name="Proprietaire de la pharmacie.", on_delete=models.CASCADE)
    medication  = models.ManyToManyField(Medication, verbose_name="Médicaments liés à la pharmacie")

    def __init__(self):
        return f"{self.parmacien.user.username} proprietaire de la pharmacie {self.nom}"
    
    def state(self):
        return self.pharmacien.is_pharmacien
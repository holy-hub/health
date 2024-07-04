from django.db import models

# Create your models here.
class Maladie(models.Model):
    """
    disease_types = {
        "Infectious Diseases"    : ["Bacterial", "Viral", "Fungal", "Parasitic"],
        "Non-Infectious Diseases": ["Cancer", "Autoimmune", "Genetic", "Neurological", "Metabolic", "Nutritional Deficiencies"],
        "Organ-Specific Diseases": ["Cardiovascular", "Respiratory", "Gastrointestinal", "Renal", "Skin"],
        "Mental Health Disorders": ["Anxiety", "Mood", "Psychotic", "Personality"],
        "Developmental Disorders": ["Neurodevelopmental", "Congenital"],
        "Environmental Diseases" : ["Toxic", "Radiation-Related"]
    }
    """
    DISEASE_TYPES = (
        ('Maladies infectieuses', 'MALADIES INFECTIEUSES'),
        ('Maladies non infectieuses', 'MALADIES NON INFECTIEUSES'),
        ('Maladies spécifiques à un organe', 'MALADIES SPÉCIFIQUES À UN ORGANE'),
        ('Troubles de la santé mentale', 'TROUBLES DE LA SANTÉ MENTALE'),
        ('Troubles du développement', 'TROUBLES DU DÉVELOPPEMENT '),
        ('Maladies environnementales', 'MALADIES ENVIRONNEMENTALES'),
    )
    nom = models.CharField(max_length=100, verbose_name="Nom de la maladie")
    nom_scientiste = models.CharField(max_length=150, verbose_name="Nom Scientifique de la maladie")
    description = models.TextField(verbose_name="Description de la maladie")
    symptomes = models.TextField(verbose_name="Symptômes de la maladie")
    causes = models.TextField(verbose_name="Causes de la maladie")
    consequences = models.TextField(verbose_name="Conséquences de la maladie")
    disease_types = models.CharField(choices=DISEASE_TYPES, max_length=250)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.nom} ayant {len(self.medication)} medications comme solution pour y remedier."

class Medication(models.Model):
    nom = models.CharField(max_length=250)
    role = models.TextField(verbose_name="Les effets de ce medicament.")
    prix = models.PositiveIntegerField(default=0)
    ill = models.ForeignKey(Maladie, verbose_name="", on_delete=models.CASCADE)
    image = models.FileField(upload_to="image/produits/", max_length=255)

    def __str__(self):
        return f"{self.nom} à {self.prix} F CFA, reduit les effets de la maladie {self.ill.nom}."

    def get_price(self):
        return f"{self.prix} F CFA" 

class Pharmacie(models.Model):
    nom = models.CharField(max_length=250, verbose_name="Nom de la pharmacie.")
    description = models.TextField(verbose_name="Situer la pharmacie", null=True)
    location = models.URLField(max_length=200, verbose_name="Coordonnées de la pharmacie.", null=True)
    pharmacien = models.ForeignKey('authentification.Utilisateur', related_name='pharmacies', verbose_name="Proprietaire de la pharmacie.", on_delete=models.CASCADE)
    medications = models.ManyToManyField(Medication, verbose_name="Médicaments liés à la pharmacie")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.pharmacien.user.username} proprietaire de la pharmacie {self.nom}"

    def save(self, *args, **kwargs):
        if self.pharmacien.is_pharmacien:
            super().save(*args, **kwargs)

    def get_medication(self):
        return [str(medication) for medication in self.medications]

from django.db import models
import qrcode
from io import BytesIO
from django.core.files import File
from PIL import Image

class Pelerin(models.Model):
    VOCATION_CHOICES = [
        ('LAIC', 'Laïc'),
        ('PRETRE', 'Prêtre'),
        ('RELIGIEUSE', 'Religieuse'),
        ('SEMINARISTE', 'Séminariste'),
        ('EVEQUE', 'Évêque'),
    ]

    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    date_naissance = models.DateField()
    diocese = models.CharField(max_length=100)
    paroisse = models.CharField(max_length=100)
    vocation = models.CharField(max_length=20, choices=VOCATION_CHOICES, default='LAIC')
    telephone = models.CharField(max_length=15, help_text="+224XXXXXXXXX")
    email = models.EmailField(blank=True)
    
    # Paiement
    a_paye = models.BooleanField(default=False)
    reference_paiement = models.CharField(max_length=100, blank=True, null=True)
    mode_paiement = models.CharField(max_length=50, blank=True, null=True)
    
    # Système
    qr_code = models.ImageField(upload_to='qr_codes', blank=True)
    date_inscription = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        # Génération automatique du QR Code à l'enregistrement
        qrcode_img = qrcode.make(f"PELERIN-{self.nom}-{self.telephone}")
        canvas = Image.new('RGB', (290, 290), 'white')
        canvas.paste(qrcode_img)
        fname = f'qr_code-{self.nom}.png'
        buffer = BytesIO()
        canvas.save(buffer, 'PNG')
        self.qr_code.save(fname, File(buffer), save=False)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.nom} {self.prenom}"

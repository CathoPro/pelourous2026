from django.shortcuts import render, redirect, get_object_or_404
from .models import Pelerin
from django.contrib import messages

def accueil(request):
    return render(request, 'accueil.html')

def inscription(request):
    if request.method == "POST":
        pelerin = Pelerin.objects.create(
            nom=request.POST.get('nom'),
            prenom=request.POST.get('prenom'),
            date_naissance=request.POST.get('date_naissance'),
            diocese=request.POST.get('diocese'),
            paroisse=request.POST.get('paroisse'),
            vocation=request.POST.get('vocation'),
            telephone=request.POST.get('telephone'),
            email=request.POST.get('email')
        )
        # Redirection vers paiement avec l'ID du pèlerin
        return redirect('paiement', pelerin_id=pelerin.id)
    return render(request, 'inscription.html')

def paiement(request, pelerin_id):
    pelerin = get_object_or_404(Pelerin, id=pelerin_id)
    if request.method == "POST":
        pelerin.mode_paiement = request.POST.get('mode_paiement')
        pelerin.reference_paiement = request.POST.get('reference')
        pelerin.a_paye = True # On valide provisoirement en attendant vérification admin
        pelerin.save()
        return redirect('felicitation', pelerin_id=pelerin.id)
    return render(request, 'paiement.html', {'pelerin': pelerin})

def felicitation(request, pelerin_id):
    pelerin = get_object_or_404(Pelerin, id=pelerin_id)
    return render(request, 'felicitation.html', {'pelerin': pelerin})

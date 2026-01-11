from django.urls import path
from . import views

urlpatterns = [
    path('', views.accueil, name='accueil'),
    path('inscription/', views.inscription, name='inscription'),
    path('paiement/<int:pelerin_id>/', views.paiement, name='paiement'),
    path('felicitation/<int:pelerin_id>/', views.felicitation, name='felicitation'),
]

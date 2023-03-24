from django.contrib import admin
from django.urls import path
from .views import dashboard, suppression, creation_de_quizz

app_name = 'administrateur'

urlpatterns = [
    path('dashboard/', dashboard, name="dashboard"),
    path('suppression/', suppression, name="suppression"),
    path('creation-quizz/',creation_de_quizz, name='creation_de_quizz' ),
]

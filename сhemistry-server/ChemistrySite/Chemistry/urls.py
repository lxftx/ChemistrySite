from django.urls import path

from Chemistry.views import SubstancesView, PlantsView, PlantView, SearchToLise #SearchPlant


urlpatterns = [
    path('', SubstancesView.as_view(), name='substances_list'),
    path('search/', SearchToLise, name='search_plant'),
    path('substances/page/<int:page>', SubstancesView.as_view(), name='paginator'),
    path('substances/<slug:slug_substances>', PlantsView.as_view(), name='plant_list'),
    path('substances/<slug:slug_substances>/<slug:slug_plant>', PlantView.as_view(), name='plant'),
]
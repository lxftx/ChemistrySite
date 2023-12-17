from django.urls import path

from Chemistry.views import SubstancesView, PlantsView, PlantView, SearchToLise, TestInfo, test_questions_view, show_results


urlpatterns = [
    path('', SubstancesView.as_view(), name='substances_list'),
    path('substances/page/<int:page>', SubstancesView.as_view(), name='paginator_substances'),
    path('substances/<slug:slug_substances>', PlantsView.as_view(), name='plant_list'),
    path('substances/<slug:slug_substances>/test-<int:test_id>/', TestInfo.as_view(),  name='test'),
    path('substances/<slug:slug_substances>/test/<int:test_id>', test_questions_view, name='substances_test'),
    path('substances/<slug:slug_substances>/test/<int:test_id>/results/', show_results, name='show_results'),
    path('substances/<slug:slug_substances>/page/<int:page>', PlantsView.as_view(), name='paginator_plants'),
    path('substances/<slug:slug_substances>/<slug:slug_plant>', PlantView.as_view(), name='plant'),
    path('search/', SearchToLise, name='search_plant'),
]
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404, render
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from itertools import chain

from Chemistry.models import Substances, Plant, Images


# Create your views here.

class SubstancesView(ListView):
    model = Substances
    template_name = 'Chemistry/index.html'
    extra_context = {'title': 'Главная страница'}
    paginate_by = 3


class PlantsView(ListView):
    model = Plant
    template_name = 'Chemistry/plants.html'
    context_object_name = 'plants'
    paginate_by = 5

    def get_queryset(self):
        queryset = super(PlantsView, self).get_queryset()
        substances = self.kwargs.get('slug_substances')
        return queryset.filter(category_plant__slug=substances)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(PlantsView, self).get_context_data(**kwargs)
        context['title'] = Substances.objects.get(slug=self.kwargs.get('slug_substances'))
        return context


class PlantView(DetailView):
    model = Plant
    template_name = 'Chemistry/plant.html'
    slug_url_kwarg = 'slug_plant'


    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(PlantView, self).get_context_data(**kwargs)
        context['title'] = Plant.objects.get(slug=self.kwargs.get('slug_plant'))
        context['images'] = Images.objects.filter(plant=self.kwargs.get('slug_plant'))
        return context

    def get_object(self, queryset=None):
        object = get_object_or_404(Plant, slug=self.kwargs.get('slug_plant'))
        return object

# class SearchPlant(ListView):
#     model = Plant
#     template_name = 'Chemistry/search_list.html'
#
#     def get_queryset(self):
#         queryset = super(SearchPlant, self).get_queryset()
#         name = self.request.GET.get('name')
#         return queryset.filter(
#             Q(name__contains=name.capitalize()) | Q(category_plant__contains=name.capitalize()))
#
#     def get_context_data(self, *, object_list=None, **kwargs):
#         context = super(SearchPlant, self).get_context_data(**kwargs)
#         context['title'] = self.request.GET.get('name')
#         return context

def SearchToLise(request):
    name = request.GET.get('name')
    queryset_plant = Plant.objects.filter(name__contains=name.capitalize())
    queryset_substances = Substances.objects.filter(name__contains=name.capitalize())
    # соединение двух Queryset
    queryset = list(chain(queryset_plant, queryset_substances))
    context = {
        'title': name,
        'object_list': queryset
    }
    return render(request, 'Chemistry/search_list.html', context)
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404, render, redirect
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView
from itertools import chain

from Chemistry.models import Substances, Plant, Images, Tests, Question, Answers, Decision
from .forms import DecisionForm


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
        context['tests'] = Tests.objects.filter(substances__slug=self.kwargs.get('slug_substances'))
        return context


class PlantView(DetailView):
    model = Plant
    template_name = 'Chemistry/plant.html'
    slug_url_kwarg = 'slug_plant'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(PlantView, self).get_context_data(**kwargs)
        context['title'] = Plant.objects.get(slug=self.kwargs.get('slug_plant'))
        context['images'] = Images.objects.filter(plant__slug=self.kwargs.get('slug_plant'))
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


class TestInfo(ListView):
    model = Tests
    template_name = 'Chemistry/test_info.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(TestInfo, self).get_context_data(**kwargs)
        test = Tests.objects.get(substances__slug=self.kwargs.get('slug_substances'), id=self.kwargs.get('test_id'))
        context['questions'] = Question.objects.filter(test_id=test)
        context['test'] = test
        return context

# class ListQuestion(ListView):
#     model = Question
#     template_name = 'Chemistry/test.html'
#     context_object_name = 'questions'
#
#     def get_queryset(self):
#         test = get_object_or_404(Tests, substances__slug=self.kwargs.get('slug_substances'), pk=self.kwargs.get('test_id'))
#         queryset = test.question_set.all()
#         return queryset


# def add_decision(request, slug_substances, ):
#     return render(request, 'Chemistry/test.html', context={})

def test_questions_view(request, slug_substances, test_id):
    test = Tests.objects.get(pk=test_id)
    Decision.objects.filter(test__id=test.id).delete()
    questions = test.question_set.all()

    if request.method == 'POST':
        form_list = []
        for question in questions:
            form = DecisionForm(request.POST, question=question, prefix=f'question_{question.id}')
            form_list.append((question, form))

            if form.is_valid():
                decision = form.save(commit=False)
                decision.test = test
                decision.question = question
                decision.answer = form.cleaned_data['answer']
                decision.save()
            else:
                print(form.errors)

        return redirect('show_results',slug_substances=slug_substances,  test_id=test_id)

    else:
        form_list = []
        for question in questions:
            form = DecisionForm(question=question, prefix=f'question_{question.id}')
            form_list.append((question, form))
    context = {
        'form_list': form_list,
        'questions':questions,
        'test': test
    }
    return render(request, 'Chemistry/test.html', context)


def show_results(request, slug_substances, test_id):
    test = Tests.objects.get(pk=test_id)
    questions = test.question_set.all()
    decisions = Decision.objects.filter(test=test)

    result_data = []

    for question in questions:
        decision = decisions.filter(question=question).first()
        answers = Answers.objects.filter(question=question)

        result_data.append({
            'question': question,
            'decision': decision,
            'answers': answers
        })

    context = {
        'test': test,
        'result_data': result_data,
    }

    return render(request, 'Chemistry/results.html', context)
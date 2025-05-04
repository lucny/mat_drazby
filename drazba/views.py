from django.shortcuts import render
from django.views.generic import ListView, DetailView

# Create your views here.
from .models import Predmet, Exekutor


def index(request):
    context = {
        'mesic': 'květen 2022',
        'drazby': Predmet.objects.filter(zacatek_drazby__month=5, zacatek_drazby__year=2022).order_by('zacatek_drazby')[:4]
    }
    return render(request, template_name='index.html', context=context)


class ExekutorListView(ListView):
    model = Exekutor
    template_name = 'exekutor_list.html'
    queryset = Exekutor.objects.order_by('prijmeni', 'jmeno')
    context_object_name = 'exekutori'


class ExekutorDetailView(DetailView):
    model = Exekutor
    template_name = 'exekutor_detail.html'
    context_object_name = 'exekutor'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['predmety'] = self.object.predmet_set.all()
        return context
from django.shortcuts import render

# Create your views here.
from .models import Predmet


def index(request):
    context = {
        'mesic': 'květen 2022',
        'drazby': Predmet.objects.filter(zacatek_drazby__month=5, zacatek_drazby__year=2022).order_by('zacatek_drazby')[:4]
    }
    return render(request, template_name='index.html', context=context)
from django.shortcuts import render
from django.views.generic import TemplateView


# Create your views here.


class HomeTemplateView(TemplateView):
    template_name = 'Home_Module/index.html'


def site_header(request):
    return render(request, 'site_header.html', {})


def site_footer(request):
    return render(request, 'site_footer.html', {})

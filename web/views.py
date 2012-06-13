#! -*- coding: utf-8 -*-

# Create your views here.
from django.shortcuts import render

from django.template import Context, loader
from django.http import HttpResponse, HttpResponseRedirect
from web.forms import FirstTimeUserForm


def main(request):
    sablon = loader.get_template('main.html')
    icerik = Context({'page_title': "WirGuL'e Hoş Geldiniz",'icerik' : "*sayfa icerigi"})
    yanit = sablon.render(icerik)
    return HttpResponse(yanit)


def new_user(request):
    form = FirstTimeUserForm()
    if request.method == "POST":
        form = FirstTimeUserForm(request.POST)
        return HttpResponseRedirect('')    # sonraki aktarılcak yer
    else:
        return render(request, 'form/form.html', {
            'form': form,    })
#! -*- coding: utf-8 -*-

# Create your views here.
from django.shortcuts import render

from django.template import Context, loader
from django.http import HttpResponse, HttpResponseRedirect
from web.forms import FirstTimeUserForm
from django.template.context import RequestContext
from django.shortcuts import render_to_response

def main(request):
    context = dict()
    context['page_title'] = "WirGuL'e Hoş Geldiniz"
    return render_to_response("main/main.html",
        context_instance=RequestContext(request, context))


def new_user(request):
    context = dict()
    form = FirstTimeUserForm()
    if request.method == "POST":
        form = FirstTimeUserForm(request.POST)
        return HttpResponseRedirect('')    # sonraki aktarılcak yer
    else:
        context['form'] = form
        return render_to_response("new_user/form.html",
            context_instance=RequestContext(request, context))

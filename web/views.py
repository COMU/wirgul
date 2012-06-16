#! -*- coding: utf-8 -*-

# Create your views here.

from django.http import HttpResponseRedirect
from web.forms import FirstTimeUserForm,FirstTimeUser
from web.models import Faculty,Department
from django.template.context import RequestContext
from django.shortcuts import render_to_response
from utils.utils import generate_url_id

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
        if form.is_valid():
            human = True
            # POST degiskenlerini al
            name = request.POST['name']
            middle_name  = request.POST['middle_name']
            surname  = request.POST['surname']
            email = request.POST['email']
            faculty_id = request.POST['faculty']
            department_id = request.POST['department']

            #url idye kadar al
            # url_id uret, generate_url_id(20)
            #first_time_obj, created = FirstTimeUser.objects.get_or_create(name=, surname=, ...)
         #   firs_time_obj, created =FirstTimeUser.objects.get_or_create(name=name,middle_name=middle_name,surname=surname,department=department,faculty=faculty)
          ##  if created:
         #       first_time_obj.url_id = url_id
           #     first_time_obj.save()
                # mail atacaksin
            #    pass
            #else:
                # formu birden fazla kere doldurmaya çalisan insan modeli
                # onay epostasını tekrar gondermek icin sayfaya yonlendirmece
             #   pass

        else:
            context['form'] = form
            return render_to_response("new_user/form.html",
            context_instance=RequestContext(request, context))
    else:
        context['form'] = form
        return render_to_response("new_user/form.html",
            context_instance=RequestContext(request, context))

def get_departments(request):
    faculty_id = request.POST['id']
    f = Faculty.objects.get(id=id)
    departments = Department.objects.filter(faculty=f)
    for department in departments:
        s = "<option> department </option>"

   
    pass




#! -*- coding: utf-8 -*-
from utils.utils import send_email,generate_url_id,ldap_add_new_user
from django.http import HttpResponse
from web.forms import FirstTimeUserForm,FirstTimeUser
from web.models import Faculty,Department,UrlId
from django.template.context import RequestContext
from django.shortcuts import render_to_response
from django.core.urlresolvers import reverse
from django.db import connection

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
            name = request.POST['name']
            middle_name  = request.POST['middle_name']
            surname  = request.POST['surname']
            email = request.POST['email']
            faculty_id = request.POST['faculty']
            department_id = request.POST['department']
            url_ = generate_url_id()
            urlid_obj,created=UrlId.objects.get_or_create(url_id=url_)
            department = Department.objects.get(id=int(department_id))
            cursor = connection.cursor()
            cursor.execute("set foreign_key_checks = 0")
            faculty = Faculty.objects.get(id=int(faculty_id))
            first_time_obj, created = FirstTimeUser.objects.get_or_create(name=name,middle_name=middle_name,
                surname=surname,faculty=faculty,department=department,email=email,url=urlid_obj)
            if created:
                path_ = reverse('new_user_registration_view', kwargs={'url_id':url_})
                html_content ='<html><head>'+"Sayin "+name+" "+middle_name+" "+surname+" Kablosuz basvurunuzu tamamlamak icin asagidaki linke tiklayin  "
                html_content +='<p><a href="http://127.0.0.1:8000'+path_+'">TIKLAYINIZ </a></head></html>'
                send_email(html_content,email)
                ldap_add_new_user(request)
        else:
            context['form'] = form
            context['web']  = "new_user"
            return render_to_response("new_user/form.html",
            context_instance=RequestContext(request, context))
    else:
        context['form'] = form
        context['web']  = "new_user"
        return render_to_response("new_user/form.html",
            context_instance=RequestContext(request, context))

def get_departments(request):
    faculty_id = request.POST['id']
    f = Faculty.objects.get(id=faculty_id)
    departments = Department.objects.filter(faculty=f)
    s = ""
    for department in departments:
        base = '<option value="' + str(department.id) + '">' + department.name + '</option>\n'
        s += base
    return HttpResponse(s)
    
def new_user_registration(request,url_id):
    context = dict()
    context['url_id'] = url_id
    return render_to_response("new_user/new_user_info.html",
        context_instance=RequestContext(request, context))
    

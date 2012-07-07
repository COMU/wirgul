#! -*- coding: utf-8 -*-
from utils.utils import generate_url_id,generate_passwd,add_new_user
from utils.utils import sendemail_changepasswd,send_email_confirm,upper_function
from django.http import HttpResponse
from web.forms import FirstTimeUserForm,FirstTimeUser,PasswordChangeForm,GuestUserForm,GuestUser
from web.models import Faculty,Department,UrlId
from django.template.context import RequestContext
from django.shortcuts import render_to_response


def main(request):
    context = dict()
    context['web'] = "WirGuL"
    return render_to_response("main/main.html",
        context_instance=RequestContext(request, context))

def passwordchange(request):
    context = dict()
    form = PasswordChangeForm()
    if request.method == "POST":
        form = PasswordChangeForm(request.POST)
        if form.is_valid():
            email = request.POST['email']
            try:
                email_obj = FirstTimeUser.objects.get(email = email)
            except:
                context['form'] = form
                context['web']  = "passwordchange"
                return render_to_response("passwordchange/invalid_mail.html",
                    context_instance=RequestContext(request, context))
            sendemail_changepasswd(email)
            context['form'] = form
            context['web']  = "passwordchange"
            return render_to_response("passwordchange/passwordchange_mail.html",
                context_instance=RequestContext(request, context))
        else:
            context['form'] = form
            context['web']  = "passwordchange"
            context['info'] = 'Parolamı Unuttum'
            return render_to_response("passwordchange/passwordchange.html",
                context_instance=RequestContext(request, context))
    else:
        context['form'] = form
        context['web']  = "passwordchange"
        context['info'] = 'Parolamı Unuttum'
        return render_to_response("passwordchange/passwordchange.html",
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
            faculty = Faculty.objects.get(id=int(faculty_id))
            name=upper_function(str(name))
            middle_name = upper_function(str(middle_name))
            surname = upper_function(str(surname))
            first_time_obj, created = FirstTimeUser.objects.get_or_create(name=name,middle_name=middle_name,
                surname=surname,faculty=faculty,department=department,email=email,url=urlid_obj)
            if created:
                send_email_confirm(email,url_,urlid_obj)
                context['form'] = form
                context['web']  = "new_user"
                return render_to_response("new_user/send_mail.html",
                    context_instance=RequestContext(request, context))
            else:
                context['form'] = form
                context['web']  = "new_user"
                return render_to_response("passwordchange/invalid_mail.html",
                    context_instance=RequestContext(request, context))
        else:
            context['form'] = form
            context['web']  = "new_user"
            context['info'] = 'Yeni Kullanıcı Kaydı'
            return render_to_response("new_user/form.html",
                context_instance=RequestContext(request, context))
    else:
        context['form'] = form
        context['web']  = "new_user"
        context['info'] = "Yeni Kullanıcı Kaydı"
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

def get_time(request):
    type_id = request.POST['id']
    t = GuestUser.objects.get(id=type_id)

def guest_user(request):
    context = dict()
    form = GuestUserForm()
    if request.method == "POST":
        form = GuestUserForm(request.POST)
        if form.is_valid():
           name = request.POST['name']
           middle_name = request.POST['middle_name']
           surname = request.POST['surname']
           guest_user_email = request.POST['guest_user_email']
           email = request.POST['email']
           surname = upper_function(str(surname))
           name=upper_function(str(name))
           middle_name = upper_function(str(middle_name))
        else:
            context['form'] = form
            context['web']  = "guest_user"
            context['info'] = 'Misafir Kullanıcı Kaydı'
            return render_to_response("guest_user/guest_user.html",
                context_instance=RequestContext(request, context))
    else:
        context['form'] = form
        context['web']  = "guest_user"
        context['info'] = 'Misafir Kullanıcı Kaydı'
        return render_to_response("guest_user/guest_user.html",
            context_instance=RequestContext(request, context))

def password_change_registration(request):

    pass



def new_user_registration(request,url_id):
    context = dict()
    context['url_id'] = url_id
    passwd = generate_passwd()
    if add_new_user(url_id,passwd) == 2:
        return render_to_response("new_user/new_user_info.html",
            context_instance=RequestContext(request, context))
    return render_to_response("new_user/send_mail.html",
        context_instance=RequestContext(request, context))
    

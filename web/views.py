#! -*- coding: utf-8 -*-
from utils.utils import generate_url_id,generate_passwd,add_new_user,LdapHandler,user_already_exist
from utils.utils import new_user_confirm,upper_function,change_password_confirm,change_password_info
from django.http import HttpResponse
from utils.utils import guest_user_confirm,guest_user_invalid_request,host_user_confirm
from web.forms import FirstTimeUserForm,FirstTimeUser,PasswordChangeForm,GuestUserForm,GuestUser
from web.models import Faculty,Department,UrlId
from django.template.context import RequestContext
from django.shortcuts import render_to_response


def main(request):
    context = dict()
    context['web'] = "WirGuL"
    return render_to_response("main/main.html",
        context_instance=RequestContext(request, context))

def password_change(request):
    context = dict()
    form = PasswordChangeForm()
    if request.method == "POST":
        form = PasswordChangeForm(request.POST)
        if form.is_valid():
            email = request.POST['email']
            obj = LdapHandler()
            obj.connect()
            obj.bind()
            if obj.search(email) != 1:  # egerldapta girilen mail adresindeki kayıt yoksa
                context['form'] = form
                context['web']  = "password_change"   # veri tabanının hepsini kontrol edebilir
                return render_to_response("password_change/invalid_mail.html",
                    context_instance=RequestContext(request, context))
            email_obj = FirstTimeUser.objects.get(email=email)
            url_id = str(email_obj.url_id)
            u = UrlId.objects.get(id=url_id)
            url = u.url_id # parolasını unutan kişiye ait 20 karakterli url
            change_password_confirm(email,url)
            context['form'] = form
            context['web']  = "password_change"
            return render_to_response("password_change/password_change_mail.html",
                context_instance=RequestContext(request, context))
        else:
            context['form'] = form
            context['web']  = "password_change"
            context['info'] = 'Parolamı Unuttum'
            return render_to_response("password_change/password_change.html",
                context_instance=RequestContext(request, context))
    else:
        context['form'] = form
        context['web']  = "password_change"
        context['info'] = 'Parolamı Unuttum'
        return render_to_response("password_change/password_change.html",
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
                new_user_confirm(email,url_,urlid_obj)
                context['form'] = form
                context['web']  = "new_user"
                return render_to_response("new_user/new_user_confirm.html",
                    context_instance=RequestContext(request, context))
            else:
                context['form'] = form
                context['web']  = "new_user"
                return render_to_response("password_change/invalid_mail.html",
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
           guest_user_phone = request.POST['guest_user_phone']
           surname = upper_function(str(surname))
           name=upper_function(str(name))
           middle_name = upper_function(str(middle_name))
           obj = LdapHandler()
           obj.connect()
           obj.bind()
           if obj.search(guest_user_email) == 1:  # eger kayıt olmak isteyen misafir zaten ldap'ta kayıtllıysa
               obj.unbind()
               user_already_exist(guest_user_email)
               context['form'] = form
               context['web']  = "guest_user"
               context['info'] = 'Misafir Kullanıcı Kaydı'
               return render_to_response("guest_user/guest_user_confirm.html",
                   context_instance=RequestContext(request, context))
           elif obj.search(email) != 1:   # eger misafiri olunmak istenen kişi yoksa
               obj.unbind()
               guest_user_invalid_request(email)
               context['form'] = form
               context['web']  = "guest_user"
               context['info'] = 'Misafir Kullanıcı Kaydı'
               return render_to_response("guest_user/guest_user_confirm.html",
                   context_instance=RequestContext(request, context))
           url = generate_url_id()
           guest_user_obj, created = GuestUser.objects.get_or_create(name=name,middle_name=middle_name,
               surname=surname,email=email,guest_user_email=guest_user_email,url=url,guest_user_phone=guest_user_phone)
           print "--"
           guest_user_confirm(guest_user_email) # misafir kullanıcıya ev sahibi kullanıcıya mail atıldıgının bildirilmesi
           print "wdww"
           if email.find("@comu.edu.tr") != -1:
               mail_adr = email.split("@")
               email = mail_adr[0]
               email = "".join([mail_adr[0],"@gmail.com"])
           host_user_confirm(email,guest_user_email)
           context['form'] = form
           context['web']  = "guest_user"
           context['info'] = 'Misafir Kullanıcı Kaydı'
           return render_to_response("guest_user/guest_user_confirm.html",
                   context_instance=RequestContext(request, context))
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

def guest_user_registration(request,url_id):
    g = GuestUser.objects.get(url = url_id)
    email = str(g.emai)
    name = str(g.name)
    middle_name = str(g.middle_name)
    surname = str(g.surname)
    password = generate_passwd()
    context = dict()
    context['url_id'] = url_id
    obj = LdapHandler()
    obj.connect()
    obj.bind()
    obj.add(name,middle_name,surname,email,password)
    obj.unbind()
    return render_to_response("guest_user/guest_user_info.html",
            context_instance=RequestContext(request, context))



def password_change_registration(request,url_id):
    context = dict()
    context['url_id'] = url_id
    u = UrlId.objects.get(url_id = url_id)
    f = FirstTimeUser.objects.get(url= u) # parolasını unutan kişinin mail adresini alma
    email = str(f.email)
    password = generate_passwd()
    obj = LdapHandler()
    obj.connect()
    obj.bind()
    obj.modify(password,email)
    obj.unbind()
    change_password_info(email,password)
    return render_to_response("password_change/password_change_mail.html",
        context_instance=RequestContext(request, context))

def new_user_registration(request,url_id):
    context = dict()
    context['url_id'] = url_id
    passwd = generate_passwd()
    if add_new_user(url_id,passwd) == 2:  # ldap'a ekleme yapılıyorsa gosterilen sayfa
        return render_to_response("new_user/new_user_info.html",
            context_instance=RequestContext(request, context))
    # ldap'ta zaten kayıtlıysa gosterilen sayfa
    return render_to_response("new_user/new_user_confirm.html",
        context_instance=RequestContext(request, context))
    

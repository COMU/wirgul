#! -*- coding: utf-8 -*-

import datetime
from utils.utils import generate_url_id,generate_passwd,add_new_user,LdapHandler,user_already_exist
from utils.utils import send_new_user_confirm,upper_function,send_change_password_confirm,send_change_password_info
from django.http import HttpResponse
from utils.utils import send_guest_user_confirm, send_host_user_confirm
from web.forms import FirstTimeUserForm,FirstTimeUser,PasswordChangeForm,GuestUserForm,GuestUser,PasswordChange
from web.models import Faculty,Department,Url
from django.template.context import RequestContext
from django.shortcuts import render_to_response
from django.http import Http404
from django.conf import settings

def main(request):
    context = dict()
    context['web'] = "WirGuL"
    context['main_page'] = settings.MAIN_PAGE
    context['welcome_header'] = settings.WELCOME_HEADER
    return render_to_response("main/main.html",
        context_instance=RequestContext(request, context))

def new_password(request):
    context = dict()
    context['page_title'] = "Parola Değiştirme Sayfası"
    form = PasswordChangeForm()
    if request.method == "POST":
        form = PasswordChangeForm(request.POST)
        if form.is_valid():
            email = request.POST['email']
            ldap_handler = LdapHandler()
            bind_status = False
            if ldap_handler.connect():
                bind_status = ldap_handler.bind()
            if bind_status:
                if ldap_handler.search(email) != 1:  # eger ldapta girilen mail adresindeki kayıt yoksa
                    context['form'] = form
                    context['web']  = "password_change"# veri tabanının hepsini kontrol edebilir
                    context['info'] = "password_change_invalid_mail"
                    return render_to_response("main/info.html",
                        context_instance=RequestContext(request, context))
                url = generate_url_id()
                url_obj = Url.objects.create(url_id=url, url_create_time=datetime.datetime.now())
                password_change = PasswordChange.objects.create(email=email, url=url_obj)
                send_change_password_confirm(email, url, ldap_handler)  # linkini onaylamasi icin gonderdigim mail
                ldap_handler.unbind()
                context['form'] = form
                context['web']  = "password_change"
                context['info'] = "password_change_mail_confirm"
                context['email'] = email
                return render_to_response("main/info.html",
                    context_instance=RequestContext(request, context))
        else:
            context['form'] = form
            context['web']  = "password_change"
            return render_to_response("password_change/password_change.html",
                context_instance=RequestContext(request, context))
    else:
        context['form'] = form
        context['web']  = "password_change"
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
            ldap_handler = LdapHandler()
            bind_status = False
            if ldap_handler.connect():
                bind_status = ldap_handler.bind()
            if bind_status:
                #TODO: forma epostadaki domain uzantısı için kontrol koymak lazım
                if ldap_handler.search(email) == 1: # zaten böyle bir kullanıcı kayıtlı
                    context['form'] = form
                    context['web']  = "new_user"
                    context['info'] = "new_user_already_exist"
                    context['email'] = email
                    return render_to_response("main/info.html",
                        context_instance=RequestContext(request, context))
                else:  # eğer boyle bir kullanıcı yoksa onaylama linkinin olduğu bir mail atar.
                    generated_url = generate_url_id()
                    url_obj = Url.objects.create(url_id=generated_url)
                    department = Department.objects.get(id=int(department_id))
                    faculty = Faculty.objects.get(id=int(faculty_id))
                    name=upper_function(name)
                    if middle_name:
                        middle_name = upper_function(middle_name)
                    surname = upper_function(surname)
                    first_time_obj = FirstTimeUser.objects.create(name=name, middle_name=middle_name,
                        surname=surname, faculty=faculty, department=department, email=email, url=url_obj)
                    status = send_new_user_confirm(email, generated_url, url_obj)  # onaylama linkinin olduğu mail
                    ldap_handler.unbind()
                    if status:
                        context['form'] = form
                        context['web']  = "new_user"
                        context['email'] = email
                        context['info'] = "mail_confirm" # onaylama linkini gonderdigimiz belirten mesaj
                        return render_to_response("main/info.html",
                            context_instance=RequestContext(request, context))
                    else:
                        raise Http404
        else:
            context['page_title'] = "WirGuL'e Hoş Geldiniz"
            context['form'] = form
            context['web']  = "new_user"
            return render_to_response("new_user/form.html",
                context_instance=RequestContext(request, context))
    else:
        context['page_title'] = "WirGuL'e Hoş Geldiniz"
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

def get_times(request):
    type_id = request.POST['id']

def guest_user(request):
    raise Http404
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
           ldap_handler = LdapHandler()
           bind_status = False
           if ldap_handler.connect():
               bind_status = ldap_handler.bind()
           if bind_status:
               if ldap_handler.search(guest_user_email) == 1:  # eger kayıt olmak isteyen misafir zaten ldap'ta kayıtllıysa
                   ldap_handler.unbind()
                   user_already_exist(guest_user_email)
                   context['form'] = form
                   context['web']  = "guest_user"
                   context['page_title'] = "Misafir Kullanıcı Başvurusu"
                   context['info'] = "guest_user_already_exist"
                   return render_to_response("main/info.html",
                       context_instance=RequestContext(request, context))
               url = generate_url_id()
               guest_user_obj = GuestUser.objects.create(name=name,middle_name=middle_name,
                   surname=surname,email=email,guest_user_email=guest_user_email,url=url,guest_user_phone=guest_user_phone)
               send_guest_user_confirm(guest_user_obj) # misafir kullanıcıya ev sahibi kullanıcıya mail atıldıgının bildirilmesi
               if email.find("@comu.edu.tr") != -1:
                   mail_adr = email.split("@")
                   email = mail_adr[0]
                   email = "".join([mail_adr[0],"@gmail.com"])
               send_host_user_confirm(email,guest_user_email)
               context['form'] = form
               context['web']  = "guest_user"
               context['info'] = 'mail_confirm'
               return render_to_response("main/info.html",
                       context_instance=RequestContext(request, context))
        else:
            context['form'] = form
            context['web']  = "guest_user"
            return render_to_response("guest_user/guest_user.html",
                context_instance=RequestContext(request, context))
    else:
        context['form'] = form
        context['web']  = "guest_user"
        return render_to_response("guest_user/guest_user.html",
            context_instance=RequestContext(request, context))

def guest_user_registration(request,url_id):
    g = GuestUser.objects.get(url = url_id)
    email = str(g.email)
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
    context['info'] = 'host_user_info' # konuk olunan kullanıcıya arkadaşına kullanıcı adı ve parolasının gittiğini belirtmek icin olan sayfa
    return render_to_response("main/info.html",
            context_instance=RequestContext(request, context))

def new_password_registration(request,url_id):
    context = dict()
    password = generate_passwd()
    user = None
    try:
        obj_url = Url.objects.get(url_id = url_id)
        user = PasswordChange.objects.get(url=obj_url)
    except:
        raise Http404

    ldap_handler = LdapHandler()
    status = ldap_handler.connect()
    if status:
        ldap_handler.bind()
    else:
        ldap_handler.unbind()
        raise Http404

    email = user.email
    # daha once bu linke tikladimi diye kontrol et.
    if obj_url.status: # eger bu ifade dogruysa linke daha once en az bir kez tiklamis ve parolasını değiştirmiştir.
        context['info'] = "password_change_st_true"
        context['page_title'] = "Uyarı!"
        return render_to_response("main/info.html",
            context_instance=RequestContext(request, context))
    obj_url.status = True # bu linke tiklandigini belirtmek icin statusu true yaptim.
    obj_url.save()
    #zaman aşımı aşılmış mı diye kontrol
    now = datetime.datetime.now()
    time_difference = now - obj_url.url_create_time
    if time_difference.total_seconds() <= settings.LINK_TIMEOUT:
        if ldap_handler.modify(password, email):
            send_change_password_info(email, password, ldap_handler)
            ldap_handler.unbind()
            context['info'] = "password_change_successful"
            context['email'] = email
            context['page_title'] = "Parola değiştirme başarılı"
            return render_to_response("main/info.html",
                context_instance=RequestContext(request, context))
        else:  # modify işlemi sırasında herhangi bir hata oluşursa diye kontrol eklendi
            ldap_handler.unbind()
            context['info'] = 'ldap_error'
            context['page_title'] = "Hata oluştu!"
            return render_to_response("main/info.html",
                context_instance=RequestContext(request, context))
    else:
         ldap_handler.unbind()
         context['info'] = 'expire_time'
         return render_to_response("main/info.html",
                context_instance=RequestContext(request, context))

def new_user_registration(request,url_id):
    context = dict()
    u = Url.objects.get(url_id=url_id)
    f = FirstTimeUser.objects.get(url=u)

    #zaman aşımı aşılmış mı diye kontrol
    now = datetime.datetime.now()
    time_difference = now - u.url_create_time
    if time_difference.total_seconds() > settings.LINK_TIMEOUT:
        context['info'] = 'new_user_link_timeout'
        return render_to_response("main/info.html",
            context_instance=RequestContext(request, context))

    context['url_id'] = url_id
    passwd = generate_passwd()
    ldap_handler = LdapHandler()
    status = ldap_handler.connect()
    if status:
        ldap_handler.bind()
    else:
        ldap_handler.unbind()
        raise Http404

    email = f.email
    if ldap_handler.search(email) == 1: # zaten böyle bir kullanıcı kayitli
        context['info'] = 'new_user_already_exists' # bu linke daha onceden tiklayip
        # kendisini ldap'a kaydetmis ancak tekrar tiklayip kayit olmaya calisirsa
        ldap_handler.unbind()
        return render_to_response("main/info.html",
            context_instance=RequestContext(request, context))
    elif add_new_user(f, passwd, ldap_handler):  # ldap'a ekleme yapılıyorsa gosterilen sayfa
        context['info'] = 'new_user_info'
        context['email'] = email
        ldap_handler.unbind()
        return render_to_response("main/info.html",
            context_instance=RequestContext(request, context))
    else:
        ldap_handler.unbind()
        raise Http404




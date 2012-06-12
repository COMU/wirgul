#! -*- coding: utf-8 -*-

# Create your views here.


from django.template import Context, loader
from django.http import HttpResponse

def main(request):
    sablon = loader.get_template('extend.html')
    icerik = Context({'page_title': "WirGuL'e Hoş Geldiniz",'icerik' : "*sayfa icerigi"})
    yanit = sablon.render(icerik)
    return HttpResponse(yanit)
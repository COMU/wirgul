# Create your views here.

from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template.context import RequestContext


def test(request):

    context = {'message': "ok"}
    return render_to_response("test/test.html",
                             context_instance=RequestContext(request, context))

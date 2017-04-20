from django.shortcuts import render
from django.http import *
from django.views.decorators.csrf import csrf_exempt
from .models import Url


# Create your views here.
def prepareContent(content):
    if (content[0:7] != "http://" and content[0:8] != "https://"):
        content = "http://" + content
    return content


def prepareHeadboard():
    return "<h1><DIV ALIGN=center>Url Shortening</DIV></h1><br /><hr />"


@csrf_exempt
def barra(request):
    htmlAnswer = prepareHeadboard()
    if request.method == "GET":
        htmlAnswer += "<DIV ALIGN=center>" \
            + "<form id='paginas' method='POST' action=''>" \
            + "<label> Introduce the Url you want to shorten  </label>" \
            + "<input name='name' type='text'>" \
            + "<input type='submit' value='Send'></form>" \
            + "</DIV><hr /><br>"
        htmlAnswer += "<table style='width:100%'>" \
            + "<tr>" \
            + "<th>Shortened Adress</th>" \
            + "<th>Original Adress</th>"  \
            + "</tr>"
        for ct in Url.objects.all():
            htmlAnswer += "<tr>" \
                + "<td>" + "http://localhost:1234/" + str(ct.id) + "</td>" \
                + "<td>" + ct.adress + "</td>" \
                + "</tr>"
        htmlAnswer += "</table>"
        return HttpResponse(htmlAnswer)
    elif request.method == "POST":
        try:
            page = Url.objects.get(adress=request.POST['name'])
            answer = page.id
            htmlAnswer += "The adress is already shortened, " \
                + "the id of it is: " \
                + str(answer)
            return HttpResponse(htmlAnswer)
        except Url.DoesNotExist:
            recurso = request.POST['name']
            if recurso == "":
                htmlAnswer += "<DIV ALIGN=center>" \
                    + "The resource was empty, " \
                    + "try to introduce an Url please" \
                    + "</DIV>"
                return HttpResponse(htmlAnswer)
            else:
                recurso = prepareContent(recurso)
                pagina = Url(adress=recurso)
                pagina.save()
                htmlAnswer += "The url " + recurso + " has been shortened," \
                    + " you can now use the adress http://localhost:1234/" \
                    + str(pagina.id) + " to access it"
                return HttpResponse(htmlAnswer)
    else:
        htmlAnswer += "Unknown method"
        return HttpResponseNotAllowed(htmlAnswer)


def redirectUrl(request, digit):
    htmlAnswer = prepareHeadboard()
    if request.method == 'GET':
        try:
            pagina = Url.objects.get(id=digit)
            answer = pagina.adress
            return HttpResponseRedirect(answer)
        except Url.DoesNotExist:
            htmlAnswer += "<DIV ALIGN=center>" \
                + "Page Not Found! This resource doesn't exist: " \
                + "http://localhost:1234/" + digit \
                + "</DIV>"
            return HttpResponseNotFound(htmlAnswer)
    elif request.method == 'POST':
        htmlAnswer += "<!DOCTYPE html><html><body>" \
                    + "Para crear una pagina vaya, haga click " \
                    + "<a href='localhost:1234/'> aqui</a>" \
                    + "</body></html>"
        HttpResponseNotFound(htmlAnswer)
    else:
        htmlAnswer += "Unknown method"
        return HttpResponseNotAllowed(htmlAnswer)

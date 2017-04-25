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
    return "<body background='http://www.pptgrounds.com/wp-content/uploads/2013/01/blue-corporate-ppt-business.jpg'>" \
       + "\r\n<br><h1 style='color:white;'>" \
       + "<DIV ALIGN=center>Url Shortening</DIV></h1><br />" \
       + "\r\n<br><br><br><br><br><br><br><hr />\r\n"


@csrf_exempt
def barra(request):
    htmlAnswer = prepareHeadboard()
    if request.method == "GET":
        htmlAnswer += "<DIV ALIGN=center>\r\n\t" \
            + "<form id='paginas' method='POST' action=''>\r\n\t\t" \
            + "<label> Introduce the Url you want to shorten </label>\r\n\t\t"\
            + "<input name='name' type='text'>\r\n\t\t" \
            + "<input type='submit' value='Send'>\r\n\t" \
            + "</form>\r\n" \
            + "</DIV><hr /><br>\r\n\t"
        htmlAnswer += "<table style='width:100%'>\r\n\t\t" \
            + "<tr>\r\n\t\t\t" \
            + "<th>Shortened Adress</th>\r\n\t\t\t" \
            + "<th>Original Adress</th>\r\n\t\t"  \
            + "</tr>\r\n\t\t"
        for ct in Url.objects.all():
            htmlAnswer += "<tr>\r\n\t\t\t" \
                + "<td>" + "http://localhost:1234/" + str(ct.id) \
                + "</td>\r\n\t\t\t" \
                + "<td>" + ct.adress + "</td>\r\n\t\t" \
                + "</tr>\r\n\t\t"
        htmlAnswer += "</table>\r\n</body>"
        return HttpResponse(htmlAnswer)
    elif request.method == "POST":
        try:
            page = Url.objects.get(adress=request.POST['name'])
            answer = page.id
            htmlAnswer += "\tThe adress is already shortened, " \
                + "the id of it is: " \
                + str(answer)
            return HttpResponse(htmlAnswer)
        except Url.DoesNotExist:
            recurso = request.POST['name']
            if recurso == "":
                htmlAnswer += "<DIV ALIGN=center>\r\n\t" \
                    + "The resource was empty, " \
                    + "try to introduce an Url please\r\n" \
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
            htmlAnswer += "<DIV ALIGN=center>\r\n\t" \
                + "Page Not Found! This resource doesn't exist: " \
                + "http://localhost:1234/" + digit + "\r\n"  \
                + "</DIV>"
            return HttpResponseNotFound(htmlAnswer)
    elif request.method == 'POST':
        htmlAnswer += "<!DOCTYPE html><html><body>\r\n\t" \
                    + "Para crear una pagina vaya, haga click " \
                    + "<a href='localhost:1234/'> aqui</a>\r\n" \
                    + "</body>\r\n</html>"
        HttpResponseNotFound(htmlAnswer)
    else:
        htmlAnswer += "\r\nUnknown method"
        return HttpResponseNotAllowed(htmlAnswer)

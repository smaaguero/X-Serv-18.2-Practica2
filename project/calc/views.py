from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def calculate(request, operating1, operator, operating2):
    if (operator == "+"):
        result = int(operating1) + int(operating2)
    elif(operator == "-"):
        result = int(operating1) - int(operating2)
    elif(operator == "*"):
        result = int(operating1) * int(operating2)
    elif(operator == "/"):
        try:
            result = int(operating1) / int(operating2)
        except ZeroDivisionError:
            return HttpResponse("<h1>Youve tried to divide by zero</h1>")
    answer = '<h1><body>Calculator</h1><p><b>' + operating1 + operator + operating2 + ' = ' + str(result) + '</b></p></body>'
    return HttpResponse(answer)

def notFound(request):
    answer = "<h1>I didn't understand what you have said</h1>"
    return HttpResponse(answer)

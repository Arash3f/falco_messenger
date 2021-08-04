from django.shortcuts import render

def index(request):
    return render(request , 'main_page.html' )

def information(request):
    return render(request , 'information.html' )   

def error_404_view(request , exception):
    return render(request , 'error_404.html')

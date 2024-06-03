from django.shortcuts import render

# Create your views here.
def home_view(request):
    page_title = 'Home'
    context = {'title': page_title}

    return render(request, 'home.html', context)

def cv_view(request):
    page_title = 'Currículo'
    context = {'title': page_title}

    return render(request, 'curriculo.html', context)
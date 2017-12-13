from django.shortcuts import render


def main(request):
    page = 'index'
    return render(request, 'index.pug', locals())

# Create your views here.

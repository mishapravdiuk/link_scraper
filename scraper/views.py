from django.shortcuts import render
import requests
from bs4 import BeautifulSoup
from .models import Link 
from django.http import HttpResponseRedirect


# Create your views here.

def scrape(request):

    if request.method == 'POST':
        site = request.POST.get("site_url", "")

        page = requests.get(site)
        soup = BeautifulSoup(page.text, 'html.parser')

        for link in soup.find_all('a'):
            link_address = link.get('href')
            link_text = link.string
            Link.objects.create(address=link_address, name=link_text)
        return HttpResponseRedirect('/')
    else:
        data = Link.objects.all()

    context = {
        "data": data,
    }

    return render(request, 'scraper/result.html', context=context)


def clear(request):
    Link.objects.all().delete()
    return render(request, 'scraper/result.html')
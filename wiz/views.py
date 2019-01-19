from django.shortcuts import render, HttpResponse
from urllib.request import urlopen
from .models import Item
import lxml
from lxml.html.clean import Cleaner
import json
import html


def index(request):
    return render(request, 'wiz/index.html', {'all_items': Item.objects.all()})


def search(request):
    return HttpResponse("you searched for" + request.GET['q'])


def all_items(request):
    return render(request, 'wiz/index.html', {'all_items': Item.objects.all()})


# Load all garbage items from Waste Wizard JSON into DB
def load(request):
    with urlopen('https://secure.toronto.ca/cc_sr_v1/data/swm_waste_wizard_APR?limit=1000') as response:
        data = json.loads(response.read().decode())

    cleaner = Cleaner()
    cleaner.remove_tags = ['span']

    item: dict
    for item in data:
        to_be_stored_body = html.unescape(item['body'])
        if '<ul' not in to_be_stored_body:
            to_be_stored_body = '<ul><li>' + to_be_stored_body + '</li></ul>'
        to_be_stored_body = cleaner.clean_html(to_be_stored_body)
        if not Item.objects.filter(body=to_be_stored_body).count():  # Only load if body is unique
            i = Item(body=to_be_stored_body, category=item['category'], title=item['title'],
                     keywords=item['keywords'])
            if 'id' in item.keys():  # Some items have an ID, load them if needed
                i.opt_id = item['id']
            i.save()

    return HttpResponse("Loaded items from JSON. Current item count: " + str(Item.objects.count()))


# Delete all items from DB
def delete_all(request):
    Item.objects.all().delete()
    return HttpResponse("All items deleted. Current item count: " + str(Item.objects.count()))

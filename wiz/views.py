import html
import json
import logging
from urllib.request import urlopen

from django.db.models import Q
from django.shortcuts import render, HttpResponse
from lxml.html.clean import Cleaner

from .models import Item

logger = logging.getLogger(__name__)


def index(request):
    return render(request, 'wiz/index.html', {'all_items': Item.objects.all()})


def search(request):
    query: str = (request.GET['q']).strip()
    result_items = Item.objects.filter(Q(keywords__icontains=query) | Q(title__icontains=query))
    return render(request, 'wiz/results.html', {'all_items': result_items})


def save_item(request):
    save_id = request.POST['id']
    i = Item.objects.get(pk=save_id)
    logger.error(str(i) + ' found with pk, currently is saved? ' + str(i.saved))
    i.saved = not i.saved
    i.save()
    return HttpResponse('toggled save of item ' + str(save_id))


def fav(request):
    result_items = Item.objects.filter(saved__exact=True)
    logger.error(result_items)
    return render(request, 'wiz/fav.html', {'all_items': result_items})


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

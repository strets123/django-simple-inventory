from datetime import date, timedelta
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.utils import simplejson as json
from django.views.generic.create_update import delete_object

from inventory.tracker.models import Product

def update_qty(request, product_id, qty):
    p = get_object_or_404(Product, id=product_id)
    p.update_qty(int(qty))
    return HttpResponse()

def qtys_before(request, days_before):
    d = date.today() - timedelta(int(days_before))
    return qtys_on(request, d.year, d.month, d.day)

def qtys_on(request, year, month, day):
    d = date(int(year), int(month), int(day))
    qtys = {'date': d.strftime('%Y-%m-%d')}
    qtys.update({'qtys':
        dict([(p.id, p.qty_on(d)) for p in Product.objects.all()])})
    return HttpResponse(json.dumps(qtys), mimetype="application/javascript")

def delete_product(request):
    return delete_object(request, model=Product,
        object_id=request.POST['object_id'], post_delete_redirect='/')

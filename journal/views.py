from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from django.utils import timezone
from django.db.models import Sum

from .models import Entry, Item

# Create your views here.
def stock(req):
	items = Item.objects.order_by('name')
	return render(req, 'journal/stock.html', {'items': items})

def history(req):
	entries = Entry.objects.order_by('-timestamp')
	paginator = Paginator(entries, 10)

	page = req.GET.get('page')
	page = paginator.get_page(page)

	return render(req, 'journal/history.html', {
		'entries': entries,
		'page': page,
	})

def new(req):
	if req.method == 'POST':
		personnel = req.POST.get('personnel')
		item_list = req.POST.getlist('item[]')
		qty_list = req.POST.getlist('qty[]')
		now = timezone.now()

		for item, qty in zip(item_list, qty_list):
			qty_int = int(qty)
			Entry.objects.create(
				timestamp=now,
				personnel=personnel,
				item=item,
				qty=qty_int
			)
			item_obj, _ = Item.objects.get_or_create(name=item, defaults={'qty': 0})
			item_obj.qty += qty_int
			item_obj.save()

		return redirect('history')

	items = Item.objects.values_list('name', flat=True).order_by('name')
	return render(req, 'journal/new.html', {
		'items': items,
	})
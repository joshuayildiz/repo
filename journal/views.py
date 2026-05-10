from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from django.utils import timezone

from .models import Entry

# Create your views here.
def index(req):
	entries = Entry.objects.order_by('-timestamp')
	paginator = Paginator(entries, 10)

	page = req.GET.get('page')
	page = paginator.get_page(page)

	return render(req, 'journal/index.html', {
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
			Entry.objects.create(
				timestamp=now,
				personnel=personnel,
				item=item,
				qty=int(qty)
			)
		return redirect('index')

	# TODO: get item names from calculated stock to be performant
	items = Entry.objects.values_list('item', flat=True).distinct().order_by('item')
	return render(req, 'journal/new.html', {
		'items': items,
	})
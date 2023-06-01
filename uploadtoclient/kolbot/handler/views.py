from django.shortcuts import render, redirect, reverse
from .models import Filter, Client
from django.http import JsonResponse, HttpResponse

def index(request):
    filters = Filter.objects.all()
    return render(request, 'handler/index.html', {'filters': filters})

def kolesafilters(request):
    filters = Filter.objects.all()
    data = {}
    for f in filters:
        data[f.id] = {
            'title':f.title,
            'url':f.url,
            'lastcar':f.lastcar,
            'cheap_perc':f.cheaper_perc,
            'view_count':f.view_count
        }
    return JsonResponse(data)

def kolesaclients(request):
    clients = Client.objects.all()
    data = {}
    for c in clients:
        data[c.name] = c.tgid

    return JsonResponse(data)

def updatelastcar(request):
    if request.method == 'POST':
        lastcar_from_post = request.POST.get('lcid')
        fid = request.POST.get('fid')
        try:
            current_filter = Filter.objects.get(id=fid)
        except:
            current_filter = None
        if current_filter:
            current_filter.lastcar = lastcar_from_post
            current_filter.save()
        return HttpResponse()
    else:
        return render(request, 'handler/lastcar.html', {})
    
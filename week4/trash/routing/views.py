from django.http import HttpResponse
# from django.shortcuts import render
from django.views.decorators.http import require_http_methods


def simple_route(request):
    if request.method == 'GET':
        return HttpResponse('', status=200)
    elif not request.method == 'GET':
        return HttpResponse('', status=405)
    return HttpResponse('', status=404)


def slug_route(request, slug):
    if request.method == 'GET':
        if len(slug) < 17:
            return HttpResponse(slug, status=200)
    return HttpResponse(status=404)


def sum_route(request, a, b):
    if request.method == 'GET':
        c = int(a) + int(b)
        return HttpResponse(c, status=200)
    return HttpResponse(status=404)


@require_http_methods(["GET"])
def sum_get_method(request):
    # if request.method == 'GET':
    try:
        a = request.GET[u'a']
        b = request.GET[u'b']
        c = int(a) + int(b)
        return HttpResponse(c, status=200)
    except:
        return HttpResponse(status=400)


@require_http_methods(["POST"])
def sum_post_method(request):
    try:
        a = request.GET[u'a']
        b = request.GET[u'b']
        print(a, b)
        c = int(a) + int(b)
        return HttpResponse(c, status=200)
    except:
        return HttpResponse(status=400)

def echo(request):
    method = ''
    stat = 'empty'

    d = request.GET.dict()
    if len(d.keys()) > 0:
        if request.method == 'GET':
            method = 'get '
        if request.method == 'POST':
            method = 'post '
    mas_par = ''
    for key in d.keys():
        par = d[key]
        mas_par += key + ': ' + str(par) + ' '
    if len(mas_par) == 0:
        mas_par = ' '
    if 'HTTP_X_PRINT_STATEMENT' in request.META:
        stat = request.META['HTTP_X_PRINT_STATEMENT']
    mes = '{}{}statement is {}'.format(method, mas_par, stat)
    return HttpResponse(mes, status=200)
    #     try:
    #         a = request.GET[u'a']
    #
    #         return HttpResponse(, status=200)
    #     b = request.GET[u'b']
    #     return HttpResponse(request, status=200)
    # elif request.method == 'POST':
    #     met = 'post'

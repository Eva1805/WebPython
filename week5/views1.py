# -*- coding: utf-8 -*-
import json

from django.http import HttpResponse, JsonResponse
from django.views import View
from django import forms
from .models import Item, Review
from django.contrib.auth.models import User
from datetime import date
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
import base64


class AddItemForm(forms.Form):
    title = forms.CharField(label='title', min_length=1, max_length=64, required=True)
    description = forms.CharField(label='description', min_length=1, max_length=1024, required=True)
    price = forms.IntegerField(label='price', min_value=1, max_value=1000000, required=True, initial=1)

class PostReviewForm(forms.Form):
    text = forms.CharField(label='text', min_length=1, max_length=1024, required=True)
    grade = forms.IntegerField(label='grade', min_value=1, max_value=10, required=True, initial=1)


@method_decorator(csrf_exempt, name='dispatch')
class AddItemView(View):
    """View для создания товара."""

    def post(self, request):
        try:
            context = json.loads(request.body)
            auth = request.META['HTTP_AUTHORIZATION']
            auth = base64.b64decode(auth).decode("utf-8").split(':')
            login = auth[0]
            password = auth[1]
        except json.JSONDecodeError:
            HttpResponse(status=400)
        except:
            return HttpResponse(status=401)


        try:
            user = User.objects.get(username=login)
        except User.DoesNotExist:
            return HttpResponse(status=401)

        if user.check_password(password):
            if user.is_staff:
                try:
                    form = AddItemForm(context)
                    if form.is_valid():
                        data = form.cleaned_data
                        item = Item(**data)
                        item.save()
                        id = item.id
                        data = {'id': id}
                        return JsonResponse(data, status=201)
                except Exception:
                    pass
                return HttpResponse(status=400)
            else:
                return HttpResponse(status=403)
        else:
            return HttpResponse(status=401)


@method_decorator(csrf_exempt, name='dispatch')
class PostReviewView(View):
    """View для создания отзыва о товаре."""

    def post(self, request, item_id):
        '''
        {"text": "jhvhgvhkgvhgv hgvhgv",
         "grade": "5"}
         '''
        try:
            item = Item.objects.get(id=item_id)
        except Item.DoesNotExist:
            return HttpResponse(status=404)

        try:
            context = json.loads(request.body)

            form = PostReviewForm(context)
            if form.is_valid():
                data = form.cleaned_data
                data['item'] = item
                review = Review(**data)
                review.save()
                data = {'id': review.id}
                return JsonResponse(data, status=201)
        except Exception:
            pass
        return HttpResponse(status=400)

@method_decorator(csrf_exempt, name='dispatch')
class GetItemView(View):
    """View для получения информации о товаре.

    Помимо основной информации выдает последние отзывы о товаре, не более 5
    штук.
    """

    def get(self, request, item_id):
        try:
            item = Item.objects.get(id=item_id)
        except Item.DoesNotExist:
            return HttpResponse(status=404)

        data = {}
        data['id'] = item.id
        data['title'] = item.title
        data['description'] = item.description
        data['price'] = item.price
        reviews = []
        review = Review.objects.filter(item=item.id).order_by('-id')[:5]
        n = len(review)
        if n > 0:
            for i in range(0, n):
                rev = review[i]
                review_info = {}
                review_info['id'] = rev.id
                review_info['text'] = rev.text
                review_info['grade'] = rev.grade
                reviews.append(review_info)
        # if len(reviews) != 0:
        data['reviews'] = reviews
        return JsonResponse(data, status=200)

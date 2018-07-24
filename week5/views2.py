from marshmallow import Schema, ValidationError, fields, post_load
from marshmallow.validate import Length, Range
from .models import Item, Review
from django.views import View
from django.http import HttpResponse, JsonResponse
import json
import base64
from django.contrib.auth.models import User


class ItemSchema(Schema):
    id = fields.Int(dump_only=True)
    title = fields.Str(required=True, validate=Length(1, 64))
    description = fields.Str(required=True, validate=Length(1, 1024))
    price = fields.Int(required=True, validate=Range(1, 1000000), strict=True)

    @post_load
    def make(self, data):
        return Item(**data)


class ReviewSchema(Schema):
    id = fields.Int(dump_only=True)
    grade = fields.Int(required=True, validate=Range(1, 10), strict=True)
    text = fields.Str(required=True, validate=Length(1, 1024))

    @post_load
    def make(self, data):
        return Review(**data)


class AddItemView(View):
    """View для создания товара."""

    def post(self, request):
        try:
            document = json.loads(request.body)
            schema = ItemSchema(strict=True)
        except:
            return HttpResponse(status=400)

        try:
            auth = request.META['HTTP_AUTHORIZATION']
            auth = base64.b64decode(auth).decode("utf-8").split(':')
            login = auth[0]
            password = auth[1]
            user = User.objects.get(username=login)
        except:
            return HttpResponse(status=401)

        if user.check_password(password):
            if user.is_staff:
                try:
                    # schema = ItemSchema(strict=True)
                    item = schema.load(document).data
                    item.save()
                except:
                    return HttpResponse(status=400)

                data = {'id': item.pk}
                return JsonResponse(data, status=201)
            else:
                return HttpResponse(status=403)
        else:
            return HttpResponse(status=401)

class PostReviewView(View):
    """View для создания отзыва о товаре."""

    def post(self, request, item_id):
        try:
            item = Item.objects.get(pk=item_id)
            document = json.loads(request.body)
            schema = ReviewSchema(strict=True)
            review = schema.load(document).data
            review.item = item
            review.save()
        except Item.DoesNotExist:
            return HttpResponse(status=404)
        except (json.JSONDecodeError, ValidationError):
            return HttpResponse(status=400)
        data = {'id': item.pk}
        return JsonResponse(data, status=201)

class GetItemView(View):
    """View для получения информации о товаре.

    Помимо основной информации выдает последние отзывы о товаре, не более 5
    штук.
    """

    def get(self, request, item_id):
        try:
            item = Item.objects.get(pk=item_id)
        except Item.DoesNotExist:
            return HttpResponse(status=404)
        schema = ItemSchema()
        data = schema.dump(item).data
        query = Review.objects.filter(item=item).order_by('-id')
        reviews = query[:5]
        schema = ReviewSchema(many=True)
        data['reviews'] = schema.dump(reviews).data
        return JsonResponse(data, status=200)
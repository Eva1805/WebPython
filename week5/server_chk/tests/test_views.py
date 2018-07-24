import json

from somemart.models import Item, Review
import requests

class TestViews(object):

    def test_post_item(self, client, db):
        """/api/v1/goods/ (POST) сохраняет товар в базе."""
        url = '/api/v1/goods/'
        data = json.dumps({
            'title': 'Сыр "Российский"',
            'description': 'Очень вкусный сыр, да еще и российский.',
            'price': '10'
        })
        response = client.post(url, data=data, content_type='application/json')
        assert response.status_code == 201
        document = response.json()
        # Объект был сохранен в базу
        item = Item.objects.get(pk=document['id'])
        assert item.title == 'Сыр "Российский"'
        assert item.description == 'Очень вкусный сыр, да еще и российский.'
        assert item.price == 10

    def test_post_review(self, client, db):
        """/api/v1/goods/ (POST) сохраняет товар в базе."""
        i = 1
        flag = True
        while flag:
            try:
                item = Item.objects.get(id=i)
                flag = False
            except:
                i += 1
                print(i)

        url = '/api/v1/goods/{}/reviews/'.format(str(i))
        data = json.dumps({
            'text': 'Очень вкусный сыр!',
            'grade': '10'
        })
        response = client.post(url, data=data, content_type='application/json')
        assert response.status_code == 201
        document = response.json()
        # Объект был сохранен в базу
        review = Review.objects.get(pk=document['id'])
        assert review.text == 'Очень вкусный сыр!'
        assert review.grade == 10

a = TestViews()
a.test_post_review(requests, {})
from __future__ import absolute_import, unicode_literals
from celery import task
from django.core.mail import send_mail
from coursera_house.settings import SMART_HOME_API_URL, SMART_HOME_ACCESS_TOKEN, EMAIL_RECEPIENT
import requests
import json
from .models import Setting

@task()
def smart_home_manager():
    # Здесь ваш код для проверки условий
    headers = {'Authorization': 'Bearer ' + SMART_HOME_ACCESS_TOKEN}
    context = {}
    try:
        result = json.loads(requests.get(SMART_HOME_API_URL, headers=headers).text)
    except Exception as ex:
        context['errors'] = str(ex)
        context['status'] = 502
        return context

    if result['status'] == 'ok':
        for line in result['data']:
            context[line['name']] = line['value']

        res = {'controllers': []}

        if context['leak_detector']:
            send_mail(
                'Умный дом',
                'Обнаружена протечка воды!',
                EMAIL_RECEPIENT,
                [EMAIL_RECEPIENT]
            )

            if context['cold_water']:
                res['controllers'].append({'name': 'cold_water', 'value': False})
                context['cold_water'] = False
            if context['hot_water']:
                res['controllers'].append({'name': 'hot_water', 'value': False})

        if context['cold_water'] and not context['smoke_detector']:
            water_bd = Setting.objects.get(controller_name='hot_water_target_temperature').value
            if not context['boiler_temperature']:
                context['boiler_temperature'] = 0
            if context['boiler_temperature'] < water_bd * 0.9 and not context['boiler']:
                res['controllers'].append({'name': 'boiler', 'value': True})

            if context['boiler_temperature'] >= water_bd * 1.1 and context['boiler']:
                res['controllers'].append({'name': 'boiler', 'value': False})
            if context['washing_machine'] == 'broken':
                res['controllers'].append({'name': 'washing_machine', 'value': 'off'})
        else:
            if context['boiler']:
                res['controllers'].append({'name': 'boiler', 'value': False})
            if context['washing_machine'] != 'off':
                res['controllers'].append({'name': 'washing_machine', 'value': 'off'})
                context['washing_machine'] = 'off'

        if not context['smoke_detector']:
            bedroom_bd = Setting.objects.get(controller_name='bedroom_target_temperature').value
            if not context['bedroom_temperature']:
                context['bedroom_temperature'] = 0
            if not context['air_conditioner'] and context['bedroom_temperature'] > bedroom_bd * 1.1:
                res['controllers'].append({'name': 'air_conditioner', 'value': True})
            if context['air_conditioner'] and context['bedroom_temperature'] < bedroom_bd * 0.9:
                res['controllers'].append({'name': 'air_conditioner', 'value': False})
        else:
            if context['air_conditioner']:
                res['controllers'].append({'name': 'air_conditioner', 'value': False})
            if context['bedroom_light']:
                res['controllers'].append({'name': 'bedroom_light', 'value': False})
                context['bedroom_light'] = False
            if context['bathroom_light']:
                res['controllers'].append({'name': 'bathroom_light', 'value': False})
                context['bathroom_light'] = False
            if context['washing_machine'] != 'off':
                res['controllers'].append({'name': 'washing_machine', 'value': 'off'})

        if context['curtains'] != 'slightly_open':
            if context['outdoor_light'] < 50 and not context['bedroom_light']:
                if context['curtains'] != 'open':
                    res['controllers'].append({'name': 'curtains', 'value': 'open'})
            if (context['outdoor_light'] > 50 or context['bedroom_light']):
                if context['curtains'] != 'close':
                    res['controllers'].append({'name': 'curtains', 'value': 'close'})

        context = {}
        if res['controllers'] != []:
            try:
                result = json.loads(requests.post(SMART_HOME_API_URL, data=json.dumps(res), headers=headers).text)
                if result['status'] == 'ok':
                    return result
                else:
                    context['errors'] = result['message']
                    context['status'] = 502
                    return context
            except Exception as ex:
                context['errors'] = str(ex)
                context['status'] = 502
                return context
        return result

    else:
        context['errors'] = result['message']
        context['status'] = 502
        return context


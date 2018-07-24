from django.urls import reverse_lazy
from django.views.generic import FormView
from .models import Setting
from .form import ControllerForm
from .tasks import smart_home_manager
from coursera_house.settings import SMART_HOME_API_URL, SMART_HOME_ACCESS_TOKEN
from django.http import HttpResponse
import requests
import json


class ControllerView(FormView):
    form_class = ControllerForm
    template_name = 'core/control.html'
    success_url = reverse_lazy('form')
    headers = {'Authorization': 'Bearer {}'.format(SMART_HOME_ACCESS_TOKEN)}

    def get_context_data(self, **kwargs):
        context = super(ControllerView, self).get_context_data()
        context['data'] = {}
        result = smart_home_manager()
        if result['status'] == 'ok':
            for line in result['data']:
                context['data'][line['name']] = line['value']
            return context
        else:
            return HttpResponse(status=502)

    def get_initial(self):
        data = {}
        bedroom_target_temperature = Setting.objects.get_or_create(label='Желаемая температура в спальне',
                                                                   controller_name='bedroom_target_temperature')
        if bedroom_target_temperature[1]:
            bedroom_target_temperature[0].value = 21
            bedroom_target_temperature[0].save()
        data['bedroom_target_temperature'] = bedroom_target_temperature[0].value

        hot_water_target_temperature = Setting.objects.get_or_create(label='Желаемая температура горячей воды',
                                                                     controller_name='hot_water_target_temperature')
        if hot_water_target_temperature[1]:
            hot_water_target_temperature[0].value = 80
            hot_water_target_temperature[0].save()
        data['hot_water_target_temperature'] = hot_water_target_temperature[0].value
        try:
            result = json.loads(requests.get(SMART_HOME_API_URL, headers=self.headers).text)
            if result['status'] == 'ok':
                data['bedroom_light'] = result['data'][1]['value']
                data['bathroom_light'] = result['data'][8]['value']
            else:
                message = 'Status: {}. Errors: {}'.format(result['status'], result['message'])
                return HttpResponse(message, status=502)
        except Exception as ex:
            return HttpResponse(str(ex), status=502)
        return data

    def form_valid(self, form):
        if form.is_valid():
            data = form.cleaned_data

            bedroom_target_temperature = Setting.objects.get_or_create(label='Желаемая температура в спальне',
                                                                       controller_name='bedroom_target_temperature')[0]
            bedroom_target_temperature.value = data['bedroom_target_temperature']
            bedroom_target_temperature.save()

            hot_water_target_temperature = Setting.objects.get_or_create(label='Желаемая температура горячей воды',
                                                                         controller_name='hot_water_target_temperature')[0]
            hot_water_target_temperature.value = data['hot_water_target_temperature']
            hot_water_target_temperature.save()
            # try:
            result = json.loads(requests.get(SMART_HOME_API_URL, headers=self.headers).text)
            res = {'controllers': []}
            if result['status'] == 'ok':
                if result['data'][1]['value'] != data['bedroom_light']:
                    res['controllers'].append({'name': 'bedroom_light', 'value': data['bedroom_light']})
                if result['data'][8]['value'] != data['bathroom_light']:
                    res['controllers'].append({'name': 'bathroom_light', 'value': data['bathroom_light']})
            else:
                message = 'Status: {}. Errors: {}'.format(result['status'], result['message'])
                return HttpResponse(message, status=502)

            if res['controllers'] != []:
                result = json.loads(requests.post(SMART_HOME_API_URL, data=json.dumps(res), headers=self.headers).text)
                if result['status'] != 'ok':
                    message = 'Status: {}. Errors: {}'.format(result['status'], result['message'])
                    return HttpResponse(message, status=502)
        return super(ControllerView, self).form_valid(form)

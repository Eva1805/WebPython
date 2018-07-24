from django import forms


class ControllerForm(forms.Form):
    bedroom_target_temperature = forms.IntegerField(label='Температура в спальне', min_value=16, max_value=50, initial=21)
    hot_water_target_temperature = forms.IntegerField(label='Температура горячей воды', min_value=24, max_value=90, initial=80)
    bedroom_light = forms.BooleanField(label='Свет в спальне', initial=False, required=False)
    bathroom_light = forms.BooleanField(label='Свет в ванной', initial=False, required=False)

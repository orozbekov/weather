import requests
from django.views.generic import TemplateView


class IndexView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = dict()
        query_params = self.request.GET
        city = query_params.get('search_city', '')
        response = requests.get(
            f"https://api.openweathermap.org/data/2.5/weather?q={city}"
            f"&appid=d8c5f4b1291c5afe2847506a5c18ac43"
            f"&units=metric"
            f"&lang=ru")
        if response.status_code == 200:
            content = dict(response.json())
            temperature = content['main']['temp']
            weather_description = content['weather'][0]['description'].capitalize()
            temp_max = content['main']['temp_max']
            temp_min = content['main']['temp_min']
            city_name = content['name']
            feels_like = content['main']['feels_like']
            icon = content['weather'][0]['icon']
            icon_img = f"https://openweathermap.org/img/w/{icon}.png"

            context['target_city'] = city_name
            context['city_temp'] = temperature
            context['weather_description'] = weather_description
            context['temp_max'] = temp_max
            context['temp_min'] = temp_min
            context['feels_like'] = feels_like
            context['weather_icon'] = icon_img
        elif response.status_code == 404:
            content = dict(response.json())
            message = content['message'].capitalize()

            context['message'] = message
        return context


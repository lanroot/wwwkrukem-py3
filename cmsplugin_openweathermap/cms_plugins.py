from urllib.request import urlopen, URLError, HTTPError
from socket import timeout
import json
from cms.plugin_pool import plugin_pool
from cms.plugin_base import CMSPluginBase
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from django.core.urlresolvers import reverse
from django.core.cache import cache

def degToCompass(num):
    val=int((num/22.5)+.5)
#    arr=["N","NNE","NE","ENE","E","ESE", "SE", "SSE","S","SSW","SW","WSW","W","WNW","NW","NNW"]
    arr=["Северный","СевСевВост","СевВосточный","ВостСевВост","Восточный","ВостЮгоВост", "ЮгоВосточный", "ЮгоЮгоВост","Южный","ЮгоЮгоЗап","ЮгоЗападный","ЗапЮгЗап","Западный","ЗапСевЗап","СевЗападный","СевСевЗап"]
    return arr[(val % 16)]


class OpenWeatherMapPlugin(CMSPluginBase):
    name = _("Open Weather Map ")
    render_template = "cmsplugin_openweathermap/local_weather.html"
    
    def render(self, context, instance, placeholder):
        urltimeout = 3
        request = context['request']
        user_ip_address = request.META['REMOTE_ADDR']
        cache_key = 'wunderground_result_%s' % user_ip_address
        openweathermap_key = settings.OPENWEATHERMAP_KEY
        weather_url = 'http://api.openweathermap.org/data/2.5/weather?q=Kemerovo,ru&APPID=8ebb785926088d2bf4fa3ef8b1d3ae43&units=metric&lang=ru'
        weather_info = cache.get(cache_key)
        if not weather_info:
            try:
                openweathermap_response = urlopen(weather_url, timeout=urltimeout)
            except (timeout, HTTPError, URLError):
                weather_info = "no data"
            else:
                weather_info_json = openweathermap_response.read().decode('utf-8')
                weather_info = json.loads(weather_info_json)
#                if weather_info['wind']['deg']:
#                    weather_info['wind']['direction'] = degToCompass(weather_info['wind']['deg'])
#                else:
#                    weather_info['wind']['deg'] =  'N/A'
#                    weather_info['wind']['direction'] =  'N/A'

            cache.set(cache_key, weather_info, getattr(settings, 'OPENWEATHERMAP_CACHE_DURATION', 60*60))
            
        context.update({
            'instance': instance,
            'weather_info': weather_info,
        })
        return context

plugin_pool.register_plugin(OpenWeatherMapPlugin)

from urllib.request import urlopen, URLError, HTTPError
from socket import timeout
import json
from cms.plugin_pool import plugin_pool
from cms.plugin_base import CMSPluginBase
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from django.core.urlresolvers import reverse
from django.core.cache import cache

class CurrentWeatherPlugin(CMSPluginBase):
    name = _("Current Local Weather")
    render_template = "cmsplugin_wunderground/local_weather.html"
    
    def render(self, context, instance, placeholder):
        urltimeout = 3
        request = context['request']
        user_ip_address = request.META['REMOTE_ADDR']
        if user_ip_address == '127.0.0.1':
            user_ip_address = '68.70.92.82'
        cache_key = 'wunderground_result_%s' % user_ip_address
        wunderground_key = settings.WUNDERGROUND_KEY
#        weather_url = 'http://api.wunderground.com/api/%s/geolookup/conditions/lang:RU/q/autoip.json?geo_ip=%s' % (wunderground_key, user_ip_address)
        weather_url = 'http://api.wunderground.com/api/%s/geolookup/conditions/lang:RU/q/Russia/Kemerovo.json' % (wunderground_key)
        weather_info = cache.get(cache_key)
        if not weather_info:
            try:
                wunderground_response = urlopen(weather_url, timeout=urltimeout)
            except (timeout, HTTPError, URLError):
                weather_info = "no data"
#            else:
#                weather_info_json = wunderground_response.read().decode('utf-8')
#                weather_info = json.loads(weather_info_json)
#                wind_kph = weather_info['current_observation']['wind_kph']
#                weather_info['current_observation']['wind_ms'] = ("%2d" % (wind_kph * 0.277778))
            cache.set(cache_key, weather_info, getattr(settings, 'WUNDERGROUND_CACHE_DURATION', 60*60))
            
        context.update({
            'instance': instance,
            'ip': user_ip_address,
            'weather_info': weather_info,
        })
        return context

plugin_pool.register_plugin(CurrentWeatherPlugin)

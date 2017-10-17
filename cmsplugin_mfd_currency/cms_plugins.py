from urllib.request import urlopen, URLError, HTTPError
from socket import timeout
from cms.plugin_pool import plugin_pool
from cms.plugin_base import CMSPluginBase
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from django.core.urlresolvers import reverse
from django.core.cache import cache

class MfdCurrencyPlugin(CMSPluginBase):
    name = _("MFD.RU Currency")
    render_template = "cmsplugin_mfd_currency/mfd_currency.html"
    
    def render(self, context, instance, placeholder):
        urltimeout = 3
        request = context['request']

        cache_key_mfdcurrency = 'mfdcurrency_result'
        mfdcurrency_url = 'http://mfd.ru/services/informers/currency/'
        mfdcurrency = cache.get(cache_key_mfdcurrency)

        cache_key_mfdtable = 'mfdtable_result'
        mfdtable_url = 'http://mfd.ru/marketdata/tables/handlerjs.ashx?sources=53$|19$|13$|29$'
        mfdtable = cache.get(cache_key_mfdtable)

        cache_key_mfdimage= 'mfdimage_result'
        mfdimage_url='http://mfd.ru/marketdata/charts/handler.ashx?id=1954&width=255&height=150&lineColor=%232c87b7&backgroundColor=%23eff6fb&gridColor=%23a3c3cc&axisColor=%23617db4&textColor=%2318479b'
        mfdimage = cache.get(cache_key_mfdimage)

        if not mfdcurrency:
            try:
                mfdcurrency_response = urlopen(mfdcurrency_url, timeout=urltimeout)
            except (timeout, HTTPError, URLError):
                mfdcurrency = "no data"
            else:
                mfdcurrency = mfdcurrency_response.read()
            cache.set(cache_key_mfdcurrency, mfdcurrency, getattr(settings, 'MFD_CURRENCY_CACHE_DURATION', 60*60))

        if not mfdtable:
            try:
                mfdtable_response = urlopen(mfdtable_url, timeout=urltimeout)
            except (timeout, HTTPError, URLError):
                mfdtable = "no data"
            else:
                mfdtable = mfdtable_response.read()
            cache.set(cache_key_mfdtable, mfdtable, getattr(settings, 'MFD_TABLE_CACHE_DURATION', 60*60))

        if not mfdimage:
            try:
                mfdimage_response = urlopen(mfdimage_url, timeout=urltimeout)
            except (timeout, HTTPError, URLError):
                mfdimage = "no data"
            else:
                mfdimage = mfdimage_response.read()
                f = open("media/downloads/mfdimage.png", "wb")
                f.write(mfdimage)
                f.close()
            cache.set(cache_key_mfdimage, 'Exist', getattr(settings, 'MFD_IMAGE_CACHE_DYRATION', 60*5))

        context.update({
            'instance': instance,
            'mfdcurrency': mfdcurrency,
            'mfdtable': mfdtable,
            'mfdimage': mfdimage,
        })
        return context

plugin_pool.register_plugin(MfdCurrencyPlugin)

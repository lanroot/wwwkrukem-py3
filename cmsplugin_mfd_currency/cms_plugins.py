from urllib.request import urlopen
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
            mfdcurrency_response = urlopen(mfdcurrency_url)
            mfdcurrency = mfdcurrency_response.read()
            cache.set(cache_key_mfdcurrency, mfdcurrency, getattr(settings, 'MFD_CURRENCY_CACHE_DURATION', 60*60))

        if not mfdtable:
            mfdtable_response = urlopen(mfdtable_url)
            mfdtable = mfdtable_response.read()
            cache.set(cache_key_mfdtable, mfdtable, getattr(settings, 'MFD_TABLE_CACHE_DURATION', 60*60))

        if not mfdimage:
            mfdimage = urlopen(mfdimage_url).read()
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

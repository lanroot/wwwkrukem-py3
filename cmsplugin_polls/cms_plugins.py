from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool
from django.utils.translation import ugettext as _

from .models import PollPlugin as Plugin


class PollPlugin(CMSPluginBase):
    model = Plugin
    name = _('Poll Plugin')
    render_template = 'cms/plugins/poll.html'

    def render(self, context, instance, placeholder):
        context['poll'] = instance.poll
        context['can_vote'] = instance.poll.can_vote(context.get('request'))
        return context

plugin_pool.register_plugin(PollPlugin)

import json
from django import http
from django.views.generic import View

from .models import Poll


class Vote(View):
    def post(self, request):
        poll_id = request.POST.get('poll')
        try:
            error = None
            poll = Poll.objects.get(id=poll_id)
        except Poll.DoesNotExist:
            error = 'Poll does not exist'
        except ValueError:
            error = 'Invalid data'
        if error:
            return http.HttpResponseBadRequest(error)

        if not poll.can_vote(request):
            return http.HttpResponseForbidden('You had voted')

        choice = request.POST.get('choice')
        if choice:
            if poll.vote(choice, request):
                return http.HttpResponse('OK')
            else:
                return http.HttpResponseBadRequest('Invalid choice')
        else:
            return http.HttpResponseBadRequest('There is no choice')

    def is_ajax(self):
        return self.request.is_ajax()

    def next_page(self):
        if self.is_ajax():
            return None
        referer = self.request.META.get('HTTP_REFERER')
        return self.request.POST.get('next', referer)

    def dispatch(self, request, *args, **kwargs):
        res = super(Vote, self).dispatch(request, *args, **kwargs)
        if self.is_ajax():
            return self.to_json(res)
        next_page = self.next_page()
        return next_page and http.HttpResponseRedirect(next_page) or res

    def to_json(self, response):
        data = json.dumps({
            'status': response.status_code,
            'message': response.content,
        })
        return http.HttpResponse(
            data, status=response.status_code,
            content_type='application/json')

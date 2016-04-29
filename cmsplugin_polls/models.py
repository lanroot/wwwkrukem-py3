from cms.models import CMSPlugin
from django.db import models
from django.db.models import F
from django.utils import timezone


class Poll(models.Model):
    question = models.CharField(max_length=200)
    is_active = models.BooleanField(default=True)
    starts_at = models.DateTimeField(null=True, blank=True)
    ends_at = models.DateTimeField(null=True, blank=True)

    def __unicode__(self):
        return self.question

    @property
    def total_votes(self):
        return self.choice_set.aggregate(models.Sum('votes'))['votes__sum']

    @property
    def max_votes(self):
        return self.choice_set.aggregate(models.Max('votes'))['votes__max']

    @property
    def _voted_key(self):
        return 'cmsplugin_poll_voted_{i}'.format(i=self.id)

    def can_vote(self, request=None):
        if not self.is_active:
            return False
        if self.starts_at and self.starts_at > timezone.now():
            return False
        if self.ends_at and self.ends_at < timezone.now():
            return False
        if not request or not hasattr(request, 'session'):
            return True
        return not request.session.get(self._voted_key, False)

    def vote(self, choice, request=None):
        try:
            choice = int(choice)
        except ValueError:
            return 0
        if not self.can_vote(request):
            return 0
        rows = self.choice_set.filter(id=choice).update(votes=F('votes') + 1)
        if rows and request and hasattr(request, 'session'):
            request.session[self._voted_key] = True
        return rows

    def getrate(self, choice):
        total = self.total_votes
        if not total:
            return total
        return 100.0 * choice.votes / float(total)


class Choice(models.Model):
    poll = models.ForeignKey(Poll)
    text = models.CharField(max_length=200)
    votes = models.PositiveIntegerField(default=0)


class PollPlugin(CMSPlugin):
    poll = models.ForeignKey(Poll)

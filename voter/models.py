from django.db import models
from django.db.models import Count
import json


class Voting(models.Model):
    author = models.CharField(max_length=30)

    @property
    def get_results(self):
        temp = self.vote_set.values('option_num').annotate(co_numb=Count('option_num'))
        results = [0] * len(self.option_set.all())
        for a in temp:
            results[a['option_num']] = a['co_numb']
        return zip(self.get_options, results)

    @property
    def get_options(self):
        options = self.option_set.all()
        return options.values_list('content', flat=True)

    @property
    def get_results_json(self):
        return json.dumps(dict(self.get_results))


class Vote(models.Model):
    user_name = models.CharField(max_length=30)
    option_num = models.IntegerField(default=0, null=False)
    voting_id = models.ForeignKey(Voting, on_delete=models.CASCADE)


class Option(models.Model):
    voting_id = models.ForeignKey(Voting, on_delete=models.CASCADE)
    content = models.CharField(max_length=100)
    number = models.IntegerField(default=0, null=False)

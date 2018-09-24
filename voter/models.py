from django.db import models


class Voting(models.Model):
    author = models.CharField(max_length=30)


class Vote(models.Model):
    user_name = models.CharField(max_length=30)
    option_num = models.IntegerField(default=0, null=False)
    voting_id = models.ForeignKey(Voting, on_delete=models.CASCADE)


class Option(models.Model):
    voting_id = models.ForeignKey(Voting, on_delete=models.CASCADE)
    content = models.CharField(max_length=100)
    number = models.IntegerField(default=0, null=False)

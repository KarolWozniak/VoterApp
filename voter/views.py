from django.db.models import Count
from django.http import JsonResponse, HttpResponse
from django.template import loader
from django.shortcuts import get_object_or_404, redirect

from voter.models import Voting, Vote, Option


def get_voting(req, voting_id):
    voting = get_object_or_404(Voting.objects, pk=voting_id)
    options = voting.option_set.all()
    template = loader.get_template('voter/index.html')
    context = {
        'voting': voting,
        'options': options,
        'user': 'temp_user'
    }
    return HttpResponse(template.render(context, req))


def post_voting(req):
    template = loader.get_template('voter/editor.html')
    return HttpResponse(template.render({}, req))


def vote(req, voting_id):
    if req.method == "POST":
        option = req.POST.get('option')
    voting = get_object_or_404(Voting.objects, pk=voting_id)
    vote_obj = Vote(user_name='user', option_num=option, voting_id=voting)
    vote_obj.save()
    return JsonResponse({'response': 'OK'})


def monitor(req, voting_id):
    voting = get_object_or_404(Voting.objects, pk=voting_id)
    counted_options = Vote.objects.values('option_num')\
        .annotate(co_numb=Count('option_num'))\
        .filter(voting_id=voting)
    results = [0] * len(Option.objects.filter(voting_id=voting))
    for a in counted_options:
        results[a['option_num']] = a['co_numb']
    context = {'voting': voting,
               'results': results}
    template = loader.get_template('voter/monitor.html')
    return HttpResponse(template.render(context, req))


def add_voting(req):
    voting = Voting.objects.create(author='temp_user')
    voting.save()
    if req.method == "POST":
        option_list = req.POST.getlist('option')
        for index, value in enumerate(option_list):
            temp = Option.objects.create(voting_id=voting, content=value, number=index)
            temp.save()
    return redirect('monitor', voting_id=voting.id)

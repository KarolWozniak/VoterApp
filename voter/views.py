from django.db.models import Count
from django.http import Http404, JsonResponse, HttpResponse
from django.template import loader

from voter.models import Voting, Vote, Option


def get_voting(res, id):
    try:
        voting = Voting.objects.get(pk=id)
    except Voting.DoesNotExist:
        raise Http404("Unfortunately voting is not exist!")
    options = voting.option_set.all()
    counted_options = Vote.objects.values('option_num').annotate(co_numb=Count('option_num'))
    options_names = []
    results = [0] * len(options)
    for a in options:
        options_names.append(a.content)
    for votes in counted_options:
        results[votes['option_num']] = votes['co_numb']
    template = loader.get_template('voter/index.html')
    context = {
        'voting': voting,
        'votes': results,
        'options': options,
        'user': 'tomasz'
    }
    return HttpResponse(template.render(context, res))


def post_voting(res, author, options):
    voting = Voting.objects.create(author=author)
    voting.save()
    options = options.split(',')
    for i, a in enumerate(options):
        temp = Option.objects.create(voting_id=voting, content=a, number=i)
        temp.save()
    return JsonResponse({'id': voting.id})


def vote(res):
    if res.method == "POST":
        user = res.POST.get('user')
        option = res.POST.get('option')
        vote_id = res.POST.get('vote_id')
    try:
        voting = Voting.objects.get(pk=vote_id)
    except Voting.DoesNotExist:
        raise Http404("Unfortunately voting is not exist!")
    vote_obj = Vote(user_name=user, option_num=option, voting_id=voting)
    vote_obj.save()
    return JsonResponse({'response': 'OK'})

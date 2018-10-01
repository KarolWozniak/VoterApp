from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import DetailView
from django.views import View

from voter.models import Voting, Vote, Option


class VotingDetailView(DetailView):
    template_name = 'voter/index.html'
    model = Voting

    def post(self, req, pk):
        option = req.POST.get('option')
        voting = get_object_or_404(Voting.objects, pk=pk)
        if req.user.username is not None:
            user_name = req.user.username
        else:
            user_name = 'Anonymous'
        vote_obj = Vote(user_name=user_name, option_num=option, voting_id=voting)
        vote_obj.save()
        return redirect('monitor', pk=pk)


class MonitorVotingDetailView(LoginRequiredMixin, DetailView):
    login_url = '/accounts/login/'
    redirect_field_name = 'redirect_to'
    template_name = 'voter/monitor.html'
    model = Voting


class EditVotingView(LoginRequiredMixin, View):
    login_url = '/accounts/login/'
    redirect_field_name = 'redirect_to'

    def get(self, req):
        return render(req, 'voter/editor.html')

    def post(self, req):
        voting = Voting.objects.create(author=req.user.username)
        voting.save()
        option_list = req.POST.getlist('option')
        for index, value in enumerate(option_list):
            temp = Option.objects.create(voting_id=voting, content=value, number=index)
            temp.save()
        return redirect('monitor', pk=voting.id)


class HomepageView(View):

    def get(self, req):
        return render(req, 'voter/homepage.html')

    def post(self, req):
        voting_id = req.POST.get('VotingId')
        try:
            voting = Voting.objects.get(pk=voting_id)
        except ObjectDoesNotExist:
            return render(req, 'voter/homepage.html', {'message': 'There is no Voting with this ID'})
        return redirect('detail', pk=voting_id)

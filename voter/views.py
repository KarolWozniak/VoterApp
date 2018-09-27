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
        vote_obj = Vote(user_name='user', option_num=option, voting_id=voting)
        vote_obj.save()
        return redirect('monitor', pk=pk)


class MonitorVotingDetailView(DetailView):
    template_name = 'voter/monitor.html'
    model = Voting


class EditVotingView(View):

    def get(self, req):
        return render(req, 'voter/editor.html')

    def post(self, req):
        voting = Voting.objects.create(author='temp_user')
        voting.save()
        option_list = req.POST.getlist('option')
        for index, value in enumerate(option_list):
            temp = Option.objects.create(voting_id=voting, content=value, number=index)
            temp.save()
        return redirect('monitor', pk=voting.id)


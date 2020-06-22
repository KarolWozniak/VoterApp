from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import DetailView, ListView
from django.views import View
from django.contrib.auth.mixins import UserPassesTestMixin

from voter.models import Voting, Vote, Option

class VotingDetailView(LoginRequiredMixin, DetailView):
    template_name = 'voter/index.html'
    model = Voting
    login_url = '/accounts/login/'
    redirect_field_name = 'redirect_to'

    def post(self, req, pk):
        option = req.POST.get('option')
        voting = get_object_or_404(Voting.objects, pk=pk)
        if not (req.user.username in voting.get_users):
            vote_obj = Vote(user_name=req.user.username, option_num=option, voting_id=voting)
            vote_obj.save()
            return redirect('monitor', pk=pk)
        else:
            return render(req, self.template_name, {'voting': voting,
                                                    'error': 'You have already voted!'})


class MonitorVotingDetailView(LoginRequiredMixin, View):
    login_url = '/accounts/login/'
    redirect_field_name = 'redirect_to'

    def get(self, req, pk):
        voting = Voting.objects.get(pk=pk)
        return render(req, 'voter/monitor.html', {'voting': voting})


class EditVotingView(UserPassesTestMixin, LoginRequiredMixin, View):
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
    
    def test_func(self):
        return self.request.user.groups.filter(name='Editor').exists()


class HomepageView(View):

    def get(self, req):
        return render(req, 'voter/homepage.html')

    def post(self, req):
        voting_id = req.POST.get('VotingId')
        try:
            Voting.objects.get(pk=voting_id)
        except ObjectDoesNotExist:
            return render(req, 'voter/homepage.html', {'message': 'There is no Voting with this ID'})
        return redirect('detail', pk=voting_id)


class InfoListView(ListView):
    model = Voting
    paginate_by = 20
    template_name = 'voter/info.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(InfoListView, self).get_context_data(**kwargs)
        context['votes'] = Vote.objects.all()
        return context



from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.models import Group

from accounts import forms


class RegisterView(View):

    def get(self, req):
        if req.user.is_authenticated:
            return redirect('/voter')
        form = forms.UserForm()
        return render(req, 'accounts/register.html', {'form': form})

    def post(self, req):
        form = forms.UserForm(req.POST)
        if form.is_valid():
            user = form.save(commit=False)
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user.set_password(password)
            group = Group.objects.get(name=form.cleaned_data['group'])
            user.save()
            user.groups.add(group)
            user = authenticate(username=username, password=password)
            login(req, user)
            return redirect('/voter/edit')
        return render(req, 'accounts/register.html', {'form': form})


class LogoutView(View):

    def get(self, req):
        if req.user.is_authenticated:
            logout(req)
            return redirect('login')
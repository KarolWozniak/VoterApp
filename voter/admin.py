from django.contrib import admin

# Register your models here.

from voter.models import Voting, Option, Vote

admin.site.register(Voting)
admin.site.register(Option)
admin.site.register(Vote)

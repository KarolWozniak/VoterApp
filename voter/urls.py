
from django.urls import path

from voter import views

urlpatterns = [
    path('edit/', views.EditVotingView.as_view(), name='edit'),
    path('<pk>/', views.VotingDetailView.as_view(), name='detail'),
    path('<pk>/monitor/', views.MonitorVotingDetailView.as_view(), name='monitor'),
]

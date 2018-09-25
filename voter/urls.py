from django.urls import path

from voter import views

urlpatterns = [
    path('<int:voting_id>/', views.get_voting, name='detail'),
    path('edit/', views.post_voting, name='edit'),
    path('edit/add', views.add_voting, name='add'),
    path('<int:voting_id>/vote/', views.vote, name='vote'),
    path('<int:voting_id>/monitor/', views.monitor, name='monitor')
]

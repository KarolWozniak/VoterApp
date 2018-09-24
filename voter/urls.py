from django.urls import path

from voter import views

urlpatterns = [
    path('voting/<int:id>/', views.get_voting),
    path('voting/<str:author>&<str:options>/', views.post_voting),
    path('vote/', views.vote)
]
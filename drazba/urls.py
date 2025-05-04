from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('exekutori/', views.ExekutorListView.as_view(), name='exekutor_list'),
    path('exekutori/<int:pk>/', views.ExekutorDetailView.as_view(), name='exekutor_detail'),
]
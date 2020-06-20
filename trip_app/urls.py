from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('create_user', views.create_user),
    path('login', views.login),
    path('dashboard', views.dashboard),
    path('trips/new', views.new_trip),
    path('trips/create', views.create_trip),
    path('trips/join_trip/<int:trip_id>', views.join_trip),
    path('trips/delete_join/<int:trip_id>', views.delete_join),
    path('trips/<int:id>/delete', views.destroy),
    path('trips/edit/<int:id>', views.edit_trip),
    path('trips/update/<int:id>', views.update),
    path('trips/<int:id>', views.one_trip),
    path('log_out', views.log_out),
]
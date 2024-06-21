from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("all/", views.all, name="all"),
    path("legislation/<int:legislation_id>/", views.view_legislation, name="viewleg"),
]

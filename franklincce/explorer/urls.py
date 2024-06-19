from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("legislation/<int:legislation_id>/", views.view_legislation, name="viewleg"),
    path("import/", views.import_books, name="import_books"),
]

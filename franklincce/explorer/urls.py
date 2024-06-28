from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("all/", views.all, name="all"),
    path("stats/", views.stats, name="stats"),
    path("legislation/<int:legislation_id>/", views.view_legislation, name="viewleg"),
    path("conference/<int:conference_id>/", views.view_conference, name="viewconf"),
    path("topics/<int:classification_id>/", views.get_all_classified_by_id, name="classificationview"),
    path("topics/", views.get_all_classifications, name="classificationview"),
]

from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("all/", views.all, name="all"),
    path("stats/", views.stats, name="stats"),
    path("legislation/<int:legislation_id>/", views.view_legislation, name="viewleg"),
    path("topics/<int:model_id>/", views.get_all_classified_by_id, name="LegislationClassification.detail"),
    path("topics/", views.get_all_classifications, name="LegislationClassification"),
    path("search/", views.handle_search, name="search_legislation"),

    # these are named weirdly -- see models.py School and Country definitions
    path("schools/<int:model_id>/", views.get_all_by_school, name="School.detail"),
    path("countries/<int:model_id>/", views.get_all_by_country, name="Country.detail"),
    path("sponsors/<int:model_id>/", views.get_all_by_sponsor, name="Sponsor.detail"),
    path("categories/<int:model_id>/", views.get_all_by_category, name="Category.detail"),
    path("conference/<int:model_id>/", views.get_all_by_conference, name="LegislationBook.detail"),
    path("schools/", views.get_all_schools, name="School"),
    path("countries/", views.get_all_countries, name="Country"),
    path("groups/", views.return_groups, name="Groups"),
    path("sponsors/", views.get_all_sponsors, name="Sponsor"),
    path("categories/", views.get_all_categories, name="Category"),
    path("conference/", views.get_all_conferences, name="LegislationBook"),
]

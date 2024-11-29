from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("new", views.new, name="new"),
    path("error", views.error, name="error"),
    path("results", views.results, name="results"),
    path("wiki/<str:title>", views.entry, name="entry"),
    path("edit/<str:title>", views.edit, name="edit"),
    path("random_page", views.random_page, name="random_page")
]

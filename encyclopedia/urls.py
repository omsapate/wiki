from django.urls import path

from . import views

appname = "wiki"
urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:page_name>",views.entry_page,name="entry"),
    path("searchpage", views.search, name="searchpage"),
    path("newpage", views.newpage, name="newpage")
]

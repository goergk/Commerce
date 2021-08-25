from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("categories", views.categories, name="categories"),
    path("categories/<str:category_name>", views.category, name="category"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("watchlist/<int:listing_id>/AddOrDelete", views.AddOrDelete, name="AddOrDelete"),
    path("create", views.createListing, name="createListing"),
    path("listing/<int:listing_id>", views.listing, name="listing"),
    path("listing/<int:listing_id>/comment", views.comment, name="comment"),
    path("listing/<int:listing_id>/bid", views.bid, name="bid"),
    path("listing/<int:listing_id>/close", views.close, name="close"),
    path("newListing", views.newListing, name="newListing"),
    path("error", views.error, name="error"),
]

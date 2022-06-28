from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("watchlist", views.watchlist, name ="watchlist"),
    path("createlisting", views.create_listing, name = "createlisting"),
    path("listing<int:listing_id>", views.listing, name="listing"),
    path("updatewatchlist<int:listing_id>", views.update_watchlist, name ="update_watchlist"),
    path("placebid<int:listing_id>", views.place_bid, name ="place_bid"),
    path("addcomment<int:listing_id>", views.add_comment, name ="add_comment"),
    path("categories", views.categories, name="categories"),
    path("category<int:category_id>", views.list_by_category, name="list_by_category"),
    path("closelisting<int:listing_id>", views.close_listing, name="close_listing"),

]

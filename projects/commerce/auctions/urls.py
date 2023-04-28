from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("new_listing", views.new_listing, name="new_listing"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("categories", views.categories, name="categories"),
    path("category/<str:categoryName>", views.category, name="category"),
    path("<int:listing_id>", views.listing, name="listing"),
    path('listing/<int:listing_id>/bid_on_item', views.bid_on_item, name='bid_on_item'),
    path('listing/<int:listing_id>/comment', views.add_comment, name='add_comment'),
    path("<int:listing_id>/add_to_watchlist", views.add_to_watchlist, name="add_to_watchlist"),
    path("<int:listing_id>/remove_from_watchlist", views.remove_from_watchlist, name="remove_from_watchlist"),
    path("<int:listing_id>/close_auction", views.close_auction, name="close_auction")
]
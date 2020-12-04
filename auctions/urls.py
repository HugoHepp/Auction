from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("add_auction", views.add_auction, name="add_auction"),
    path("categories", views.categories, name="categories"),
    path("sport", views.sport, name="sport"),
    path("electronics", views.electronics, name="electronics"),
    path("mode", views.mode, name="mode"),
    path("toys", views.toys, name="toys"),
    path("addwlist/<int:item>/", views.addwlist, name="addwlist"),
    path("rmvwlist/<int:item>/", views.rmvwlist, name="remvwlist"),
    path("rmvwlistbyid/<int:item>/", views.rmvwlistbyid, name="remvwlistbyid"),
    path("watchlist/", views.watchlist, name="watchlist"),
    path("watchlist/auctions/listing/<int:item>/", views.listing, name="listing"),
    path("listing/<int:item>/", views.listing, name="listing"),
    path("bid/<int:item>/", views.bid, name="bid"),
    path("close_auction/<int:item>/", views.close_auction, name="close_auction"),
    path("add_comment/<int:item>/", views.add_comment, name="add_comment")

]

from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('register', views.register),
    path('login', views.login),
    path('logout', views.logout),
    path('success', views.success),
    path('profile', views.profile),
    path('games/new', views.new),
    path('games/create', views.create_game),
    path("games/<int:game_id>", views.show_one),
    path("grab/<int:game_id>", views.grab),
    path('games/<int:game_id>/delete', views.delete),
    path('process_message/<int:game_id>', views.post_mess),
    path('add_comment/<int:message_id>', views.post_comment),
    path('like/<int:message_id>', views.add_like),
    path('delete/<int:game_id>', views.delete_comment)
]
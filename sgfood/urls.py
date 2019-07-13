from django.urls import path
from django.contrib.auth import views as auth_view
from . import views as sgfood_view

urlpatterns = [
    path('', sgfood_view.home, name='home'),
    path('register/', sgfood_view.register, name='register'),
    path('login/', auth_view.LoginView.as_view(template_name='sgfood/login.html'), name='login'),
    path('logout/', auth_view.LogoutView.as_view(template_name='sgfood/logout.html'), name='logout'),
    path('category/', sgfood_view.category, name='category'),
    path('category/<category_id>/',
         sgfood_view.restaurant_list, name='restaurant_list'),
    path('category/<category_id>/restaurant/<restaurant_id>/',
         sgfood_view.restaurant_detail, name='restaurant_detail'),
    path('like_review', sgfood_view.like_review, name='like_review'),
    path('like_comment', sgfood_view.like_comment, name='like_comment'),
    path("review_create", sgfood_view.review_create, name="review_create"),
    path("comment_create", sgfood_view.comment_create, name="comment_create"),
    path("restaurant_rate", sgfood_view.restaurant_rate, name="restaurant_rate"),
]

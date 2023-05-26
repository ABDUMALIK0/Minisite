from django.urls import path
from . import views

urlpatterns = [
    #path('', views.index, name='index'),
    path('', views.PostList.as_view()),
    #path('<int:pk>/', views.single_post_page),
    path('<int:pk>/', views.PostDetail.as_view()),
    path('category/<str:slug>/', views.category_card_test, name='category'),
    path('create_post/', views.PostCreate.as_view(), name='category'),
    path('update_post/<int:pk>/', views.PostUpdate.as_view(), name='category'),
]

from django.urls import path
from . import views

urlpatterns = [
    #path('', views.index, name='index'),
    path('', views.PostList.as_view()),
    path('<int:pk>/new_comment/', views.new_comment, name='comment'),
    path('update_comment/<int:pk>/', views.CommentUpdate.as_view()),
    path('delete_comment/<int:pk>/', views.delete_comment),
    path('search/<str:q>/', views.PostSearch.as_view()),

    path('<int:pk>/', views.PostDetail.as_view()),
    path('category/<str:slug>/', views.category_card_test, name='category'),
    path('create_post/', views.PostCreate.as_view(), name='category'),
    path('update_post/<int:pk>/', views.PostUpdate.as_view(), name='category'),
]

from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'blog'
urlpatterns = [
    path('', views.PostList.as_view(), name='index'),
    path('<int:pk>/', views.PostDetail.as_view(), name='detail'),
    path('create/', views.PostCreate.as_view(), name='create'),
    path('update/<int:pk>/', views.PostUpdate.as_view(), name='update'),
    path('delete/<int:pk>/', views.PostDelete.as_view(), name='delete'),
    path('search/<str:q>/', views.PostSearch.as_view(), name='search'),
    path('category/<str:slug>/', views.category_card_test, name='category'),

    path('logout/', views.logout_view, name='logout'),
    path('login/', auth_views.LoginView.as_view(template_name='blog/login.html', redirect_authenticated_user=True, redirect_field_name='blog/index.html'), name='login'),
    path('signin/', views.signin_view, name='signin'),

    path('add_tag/', views.TagCreate.as_view(), name='add_tag'),
    path('add_category/', views.CategoryCreate.as_view(), name='add_category'),

    path('<int:pk>/new_comment/', views.CommentCreate.as_view(), name='comment'),
    path('update_comment/<int:pk>/', views.CommentUpdate.as_view(), name='comment_update'),
    path('delete_comment/<int:pk>/<int:post>/', views.CommentDelete.as_view(), name='comment_delete'),
    
]
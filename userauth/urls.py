from django.contrib import admin
from django.urls import path
from socialmedia import settings
from userauth import views
from django.conf.urls.static import static

urlpatterns = [
    path('',views.home),
    path('loginn/',views.loginn),
    path('signup/',views.signup),
    path('logoutt/',views.logoutt),
    path('upload',views.upload),
    path('like-post/<str:id>', views.likes, name='like-post'),
    path('#<str:id>', views.home_post),
    path('explore',views.explore),
    path('profile/<str:id_user>', views.profile),
    path('delete/<str:id>', views.delete),
    path('search-results/', views.search_results, name='search_results'),
    path('follow/', views.follow, name='follow'),
    path('submit/<str:post_id>', views.comment, name='comment'),
    path('comment/<str:id>', views.comment_show, name='comment_show'),
    path('comment/delete_comment/<str:comment_id>', views.comment_delete, name='comment_delete'),
    path('comment/edit_commentform/<str:comment_id>', views.comment_editform, name='comment_editform'),
    path('edit_comment/<str:comment_id>', views.comment_edit, name='comment_edit'),
    path('likeshow/<str:post_id>', views.show_liked_by, name='comment_edit'),
    
    
    
    
    
    
]

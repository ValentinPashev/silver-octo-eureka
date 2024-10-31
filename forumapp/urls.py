

from django.urls import path, include
from forumapp import views

urlpatterns = [
    path('', views.index, name='index'),
    path('home/', views.dashboard, name='dashboard'),
    path('create/', views.create_post, name='create_post'),
    path('search/', views.search_post, name='search_post'),
    path('<int:pk>/', include([
        path('delete/', views.delete_post_with_pk, name='delete-post'),
        path('details/', views.post_details, name='post_details'),
        path('edit/', views.edit_post, name='edit-post'),
    ]))
]



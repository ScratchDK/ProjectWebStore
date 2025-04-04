import blog.views as views
from django.urls import path
from blog.apps import BlogConfig

app_name = BlogConfig.name

urlpatterns = [
    path("post_list/", views.PostListView.as_view(), name="post_list"),
    path('post/<int:id>/', views.PostDetailView.as_view(), name='post_detail'),
    path("create_post/", views.PostCreateView.as_view(), name="create_post"),
    path("update_post/<int:id>/", views.PostUpdateView.as_view(), name="update_post"),
    path("delete_post/<int:id>/", views.PostDeleteView.as_view(), name="delete_post"),
]

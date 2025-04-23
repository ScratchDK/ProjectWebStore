from django.shortcuts import render
from django.core.mail import send_mail
from django.urls import reverse_lazy
from django.urls import reverse
from .models import Post
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
import config.settings as settings
from django.contrib.auth.mixins import LoginRequiredMixin


class PostListView(ListView):
    model = Post
    template_name = 'blog/post_list.html'
    context_object_name = 'blog'
    paginate_by = 8

    def get_queryset(self):
        return Post.objects.filter(is_published=True)


class PostDetailView(DetailView):
    model = Post
    pk_url_kwarg = 'id'
    template_name = 'blog/post_detail.html'
    context_object_name = 'post'

    def get_object(self, queryset=None):
        post = super().get_object(queryset)

        post.views_count += 1
        post.save()

        if post.views_count == 100:
            self.send_notification_email(post)

        return post

    def send_notification_email(self, post):
        subject = f'Пост "{post.title}" достиг 100 просмотров!'
        message = f'Поздравляем! Ваш пост "{post.title}" теперь имеет 100 просмотров.'
        from_email = settings.EMAIL_HOST_USER
        recipient_list = ['bloodpaperace@mail.ru']   # Получатель

        send_mail(subject, message, from_email, recipient_list)


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ["title", "content", "preview_image", "is_published"]
    template_name = 'blog/create_post.html'
    success_url = reverse_lazy('blog:post_list')


class PostUpdateView(LoginRequiredMixin, UpdateView):
    model = Post
    pk_url_kwarg = 'id'
    fields = ["title", "content", "preview_image", "is_published"]
    template_name = 'blog/update_post.html'

    def get_success_url(self):
        post_id = self.object.id
        return reverse('blog:post_detail', kwargs={'id': post_id})


class PostDeleteView(LoginRequiredMixin, DeleteView):
    model = Post
    pk_url_kwarg = 'id'
    template_name = 'blog/delete_post.html'
    success_url = reverse_lazy('blog:post_list')

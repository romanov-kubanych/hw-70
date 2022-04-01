from http import HTTPStatus

from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.http import JsonResponse
from django.views import View
from django.views.generic import CreateView, UpdateView, DeleteView
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse

from webapp.forms import CommentForm
from webapp.models import Comment, Article


class CommentCreateView(CreateView):
    model = Comment
    form_class = CommentForm
    template_name = "comments/create.html"
    permission_required = "webapp.add_article"

    def form_valid(self, form):
        article = get_object_or_404(Article, pk=self.kwargs.get('pk'))
        comment = form.save(commit=False)
        comment.author = self.request.user
        comment.article = article
        comment.save()
        return redirect('webapp:article_view', pk=article.pk)


class CommentUpdateView(PermissionRequiredMixin, UpdateView):
    model = Comment
    template_name = 'comments/update.html'
    form_class = CommentForm
    permission_required = "webapp.change_comment"

    def has_permission(self):
        return super().has_permission() or self.get_object().author == self.request.user

    def get_success_url(self):
        return reverse("webapp:article_view", kwargs={"pk": self.object.article.pk})


class CommentDeleteView(PermissionRequiredMixin, DeleteView):
    model = Comment
    permission_required = "webapp.delete_comment"

    def has_permission(self):
        return super().has_permission() or self.get_object().author == self.request.user

    def get(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)

    def get_success_url(self):
        return reverse("webapp:article_view", kwargs={"pk": self.object.article.pk})


class CommentLikeView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        comment = get_object_or_404(Comment, pk=kwargs.get('pk'))

        if request.user in comment.likes.all():
            return JsonResponse(
                {"error": 'Лайк уже поставлен'},
                status=HTTPStatus.FORBIDDEN,
            )

        comment.likes.add(request.user)
        return JsonResponse(
            {"likes_count": comment.likes.count()}
        )


class CommentUnLikeView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        comment = get_object_or_404(Comment, pk=kwargs.get('pk'))

        if not request.user in comment.likes.all():
            return JsonResponse(
                {"error": 'Нужно поставить лайк'},
                status=HTTPStatus.FORBIDDEN,
            )

        comment.likes.remove(request.user)
        return JsonResponse(
            {"likes_count": comment.likes.count()}
        )

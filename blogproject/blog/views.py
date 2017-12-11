#!/usr/bin/python
# -*- coding: UTF-8 -*-


import markdown

from django.shortcuts import render, get_object_or_404
from .models import Post, Category
from comments.forms import CommentForm
from django.views.generic import ListView, DetailView

# def index(request):
#     post_list = Post.objects.all()
#     return render(request, 'blog/index.html', context={'post_list': post_list})

class IndexView(ListView):
    model = Post
    template_name = 'blog/index.html'
    content_type = 'post_list'


# def detail(request, pk):
#     post = get_object_or_404(Post, pk=pk)
#
#     #阅读量+1
#     post.increase_views()
#
#     post.body = markdown.markdown(post.body,
#                                   extensions=[
#                                       'markdown.extensions.extra',
#                                       'markdown.extensions.codehilite',
#                                       'markdown.extensions.toc',
#                                   ])
#
#     form = CommentForm()
#     comment_list = post.comment_set.all()
#     context = {'post': post,
#                'form': form,
#                'comment_list': comment_list
#                }
#     return render(request, 'blog/detail.html', context=context)


# def archives(request, year, month):
#     post_list = Post.objects.filter(created_time__year=year,
#                                     created_time__month=month
#                                     )
#     return render(request, 'blog/index.html', context={'post_list': post_list})


class PostDetailView(DetailView):

    model = Post
    template_name = 'blog/detail.html'
    content_type = 'post'

    def get(self, request, *args, **kwargs):
        response = super(PostDetailView, self).get(request, *args, **kwargs)

        self.object.increase_views()

        return response


    def get_object(self, queryset=None):

        post = super(PostDetailView, self).get_object(queryset=None)

        post.body = Markdown.markdown(post.body,
                                      extension=[
                                          'markdown.extension.extra',
                                          'markdown.extension.codehilite',
                                          'markdown.extension.toc',
                                      ])
        return post

    def get_context_data(self, **kwargs):

        context = super(PostDetailView, self).get_context_data(**kwargs)
        form = CommentForm()
        comment_list = self.object.comment_set.all()
        context.update({
            'form': form,
            'comment_list': comment_list,
        })

        return context


class ArchivesView(ListView):
    model = Post
    template_name = 'blog/index.html'
    content_type = 'post_list'

    def get_queryset(self):
        year = self.kwarg.get('year')
        month = self.kwarg.get('month')
        return super(ArchivesView, self).get_queryset().filter(created_time__year=year,
                                                               created_time__month=month
                                                               )




# def category(request, pk):
#     cate = get_object_or_404(Category, pk=pk)
#     post_list = Post.objects.filter(category=cate)
#     return render(request, 'blog/index.html', context={'post_list': post_list})

class CategoryView(ListView):
    model = Post
    template_name = 'blog/index.html'
    content_type = 'post_list'

    def get_queryset(self):
        cate = get_object_or_404(Category, pk=self.kwarg.get('pk'))
        return super(CategoryView, self).get_queryset().filter(category=cate)
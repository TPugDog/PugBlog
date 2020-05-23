from django.shortcuts import render
from django.http import HttpResponse
from .models import Tag, Post, Category
from django.core.exceptions import ObjectDoesNotExist
# Create your views here.

# def post_list(request, category_id=None, tag_id=None):
#     content = 'post_list category_id=(category_id), tag_id=(tag_id)'.format(
#         category_id=category_id,
#         tag_id=tag_id,
#     )
#
#     return HttpResponse(content)
#
# def post_detail(requst, post_id):
#     return HttpResponse('detail')

def post_list(request, category_id=None, tag_id=None):
    if tag_id:
        try:
            tag = Tag.objects.get(id = tag_id)
        except ObjectDoesNotExist:
            post_list = []
        else:
            post_list = tag.post_set.filter(status = Post.STATUS_NORMAL)
    else:
        post_list = Post.objects.filter(status = Post.STATUS_NORMAL)
        if  category_id:
            post_list = post_list.filter(category_id = category_id)
    return render(request, 'blog/list.html', context={'post_list': post_list})

def post_detail(request, post_id=None):
    try:
        post = Post.objects.get(id=post_id)
    except ObjectDoesNotExist:
        post = None
    return render(request, 'blog/detail.html', context={'post': post})


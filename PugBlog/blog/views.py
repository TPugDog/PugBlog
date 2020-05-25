from django.shortcuts import render
from django.http import HttpResponse
from .models import Tag, Post, Category
from config.models import SideBar
from django.views.generic import DetailView
from django.core.exceptions import ObjectDoesNotExist
# Create your views here.

# def post_list(request, category_id=None, tag_id=None):
#     content = 'post_list category_id=(category_id), tag_id=(tag_id)'.format(
#         category_id=category_id,
#         tag_id=tag_id,
#     )
#
#     return HttpResponse(content)
# def post_detail(requst, post_id):
#     return HttpResponse('detail')

def post_list(request, category_id=None, tag_id=None):
    tag = None
    category = None

    if tag_id:
        post_list, tag = Post.get_by_tag(tag_id)
    elif category_id:
        post_list, category = Post.get_by_category(category_id)
    else:
        post_list = Post.latest_posts()

    # if tag_id:
    #     try:
    #         tag = Tag.objects.get(id=tag_id)
    #     except ObjectDoesNotExist:
    #         tag = None
    #         post_list = []
    # else:
    #     post_list = Post.objects.filter(status = Post.STATUS_NORMAL)
    #     if  category_id:
    #         try:
    #             category = Category.objects.get(id=category_id)
    #         except ObjectDoesNotExist:
    #             category = None
    #         else:
    #             post_list = post_list.filter(category_id = category_id)

    context = {
        'category': category,
        'tag': tag,
        'post_list': post_list,
        'sidebars': SideBar.get_all(),
    }
    context.update(Category.get_navs())
    return render(request, 'blog/list.html', context=context)

# def post_detail(request, post_id=None):
#     try:
#         post = Post.objects.get(id=post_id)
#     except ObjectDoesNotExist:
#         post = None
#
#     context = {
#         'post': post,
#         'sidebars': SideBar.get_all(),
#     }
#     context.update(Category.get_navs())
#     return render(request, 'blog/detail.html', context=context)

class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/detail.html'

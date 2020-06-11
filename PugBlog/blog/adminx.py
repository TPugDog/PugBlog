from .models import Post, Category, Tag
from django.urls import reverse
from django.utils.html import format_html
from .adminforms import PostAdminForm
from django.contrib import admin
from PugBlog.custom_site import custom_site
from PugBlog.base_admin import BaseOwnerAdmin
from xadmin.layout import Row, Fieldset, Container
from xadmin.filters import manager, RelatedFieldListFilter
import xadmin
# Register your models here.

#在新增A表数据的同时，新增一个B表数据关联到A表的新增数据上
# class PostInline:
#     form_layout = (
#         Container(
#             Row('title', 'desc'),
#         )
#     )
#     extra = 1
#     model = Post



@xadmin.sites.register(Category)
class CategoryAdmin(BaseOwnerAdmin):
    list_display = ('name', 'status', 'is_nav', 'created_time', 'post_count')
    fields = ('name', 'status', 'is_nav')

    def post_count(self,obj):
        return obj.post_set.count()

    post_count.short_description = '文章数量'
#    inlines = [PostInline, ]

@xadmin.sites.register(Tag)
class TagAdmin(BaseOwnerAdmin):
    list_display = ('name', 'status', 'created_time', 'post_count')
    fields = ('name', 'status')

    # 继承了BaseOwnerAdmin得save_models，不要重复代码
    # def save_model(self):
    #     self.new_obj.owner = self.request.user
    #     return super().save_model()

    def post_count(self,obj):
        return obj.post_set.count()

    post_count.short_description= '文章数量'

class CategoryOwnerFilter(RelatedFieldListFilter):
    @classmethod
    def test(cls, field,request, params, model, admin_view, field_path):
        return field.name == 'category'

    def __init__(self, field, request, params, model, model_admin, field_path):
        super().__init__(field, request, params, model, model_admin, field_path)
        self.lookup_choices = Category.objects.filter(owner=request.user).values_list('id', 'name')

manager.register(CategoryOwnerFilter, take_priority=True)


    # title = '分类过滤器'
    # parameter_name = 'owner_category'
    #
    # def lookups(self, request, model_admin):
    #     return Category.objects.filter(owner=request.user).values_list('id', 'name')
    #
    # def queryset(self, request, queryset):
    #     category_id = self.value()
    #     if category_id:
    #         return queryset.filter(category_id=category_id)
    #     return queryset

@xadmin.sites.register(Post)
class PostAdmin(BaseOwnerAdmin):
    # class CategoryOwnerFilter(admin.SimpleListFilter):
    #     title = '分类过滤器'
    #     parameter_name = 'owner_category'
    #
    #     def lookups(self, request, model_admin):
    #         return Category.objects.filter(owner=request.user).values_list('id', 'name')
    #
    #     def queryset(self, request, queryset):
    #         category_id = self.value()
    #         if category_id:
    #             return queryset.filter(category_id=category_id)
    #         return queryset

    form = PostAdminForm
    list_display = [
        'title', 'category', 'status',
        'created_time', 'owner', 'operator',
    ]
    list_display_links = ['status']
    list_filter = ['category']
    search_fields = ['title', 'category__name']
    
    actions_on_top = True
    #actions_on_bottom = True
    
    save_on_top = True
    
    # fields = (
    #     ('category', 'title'),
    #     'desc',
    #     'status',
    #     'content',
    #     'tag'
    # )
    form_layout = (
        Fieldset(
            '基础信息',
            Row('title', 'category'),
                'status',
                'tag',
            ),
        Fieldset(
            '内容信息',
            'desc',
            'content',
            ),
    )
    filter_vertical = ('tag', )
    def operator(self, obj):
        return format_html(
            '<a> href="{}"编辑</a>',
            reverse('xadmin:blog_post_change', args=(obj.id,))
        )
    
    operator.short_description = '操作'

    # 这种写法不适合xadmin，如何兼容看书
    # class Media:
    #     css = {
    #         'all': ("https://cdn.bootcdn.net/ajax/libs/twitter-bootstrap/4.0.0-beta.2/css/bootstrap.min.css", ),
    #     }
    #     js = ('https://cdn.bootcss.com/bootstrap/4.0.0-beta.2/js/bootstrap.bundle.js', )


# @admin.register(LogEntry, site=custom_site)
# class LogEntryAdmin(admin.ModelAdmin):
#     list_display = ['object_repr', 'object_id', 'action_flag', 'user', 'change_message']
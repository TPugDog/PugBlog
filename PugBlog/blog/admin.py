from .models import Post, Category, Tag
from django.urls import reverse
from django.utils.html import format_html
from .adminforms import PostAdminForm
from django.contrib import admin
from PugBlog.custom_site import custom_site
from PugBlog.base_admin import BaseOwnerAdmin
from django.contrib.admin.models import LogEntry
# Register your models here.

class PostInline(admin.TabularInline):
    fields = ('title', 'desc')
    extra = 1
    model = Post



@admin.register(Category)
class CategoryAdmin(BaseOwnerAdmin):
    list_display = ('name', 'status', 'is_nav', 'created_time', 'post_count')
    fields = ('name', 'status', 'is_nav')
    def save_model(self, request, obj, form, change):
        obj.owner = request.user
        return super(CategoryAdmin, self).save_model(request, obj, form, change)

    def post_count(self,obj):
        return obj.post_set.count()

    post_count.short_description = '文章数量'
    inlines = [PostInline, ]

@admin.register(Tag)
class TagAdmin(BaseOwnerAdmin):
    list_display = ('name', 'status', 'created_time', 'post_count')
    fields = ('name', 'status')
    
    def save_model(self, request, obj, form, change):
        obj.owner = request.user
        return super(TagAdmin, self).save_model(request, obj, form, change)

    def post_count(self,obj):
        return obj.post_set.count()

    post_count.short_description= '文章数量'

class CategoryOwnerFilter(admin.SimpleListFilter):
    title = '分类过滤器'
    parameter_name = 'owner_category'

    def lookups(self, request, model_admin):
        return Category.objects.filter(owner=request.user).values_list('id', 'name')

    def queryset(self, request, queryset):
        category_id = self.value()
        if category_id:
            return queryset.filter(category_id=category_id)
        return queryset

@admin.register(Post, site=custom_site)
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
    list_filter = [CategoryOwnerFilter]
    search_fields = ['title', 'category__name']
    
    action_on_top = True
    actions_on_bottom = True
    
    save_on_top = True
    
    # fields = (
    #     ('category', 'title'),
    #     'desc',
    #     'status',
    #     'content',
    #     'tag'
    # )
    fieldsets = (
        ('基础配置', {
            'description': '基础配置描述',
            'fields': (
                ('title', 'category'),
                'status',
            )
        }),
        ('内容', {
            'fields': (
                'desc',
                'content',
            ),
        }),
        ('额外信息', {
            'classes': ('collapse',),
            'fields': ('tag', ),
        })
    )
    filter_vertical = ('tag', )
    def operator(self, obj):
        return format_html(
            '<a> href="{}"编辑</a>',
            reverse('cus_admin:blog_post_change', args=(obj.id,))
        )
    
    operator.short_description = '操作'

    # class Media:
    #     css = {
    #         'all': ("https://cdn.bootcdn.net/ajax/libs/twitter-bootstrap/4.0.0-beta.2/css/bootstrap.min.css", ),
    #     }
    #     js = ('https://cdn.bootcss.com/bootstrap/4.0.0-beta.2/js/bootstrap.bundle.js', )

@admin.register(LogEntry, site=custom_site)
class LogEntryAdmin(admin.ModelAdmin):
    list_display = ['object_repr', 'object_id', 'action_flag', 'user', 'change_message']
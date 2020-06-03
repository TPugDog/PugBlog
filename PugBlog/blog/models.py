from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
import mistune
# Create your models here.

class Category(models.Model):

    def __str__(self):
        return self.name

    @classmethod
    def get_navs(cls):
        categories = cls.objects.filter(status=cls.STATUS_NORMAL)
        nav_categries = []
        normal_categories = []
        for cate in categories:
            if cate.is_nav:
                nav_categries.append(cate)
            else:
                normal_categories.append(cate)

        return {
            'navs': nav_categries,
            'categories': normal_categories,
        }

    STATUS_NORMAL = 1
    STATUS_DELETE = 0
    STATUS_ITEM = (
        (STATUS_NORMAL, '正常'),
        (STATUS_DELETE, '删除'),
    )

    name = models.CharField(max_length=50, verbose_name='名称')
    status = models.PositiveIntegerField(default=STATUS_NORMAL,
                                         choices=STATUS_ITEM, verbose_name='状态')
    is_nav = models.BooleanField(default=False, verbose_name='是否为导航')
    owner = models.ForeignKey(User, verbose_name='作者', on_delete=None)
    created_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    objects = models.Manager()
    class Meta:
        verbose_name = verbose_name_plural = '分类'

class Tag(models.Model):

    def __str__(self):
        return self.name

    STATUS_NORMAL = 1
    STATUS_DELETE = 0
    STATUS_ITEM = (
        (STATUS_NORMAL, '正常'),
        (STATUS_DELETE, '删除'),
    )

    name = models.CharField(max_length=10, verbose_name='名称')
    status = models.PositiveIntegerField(default=STATUS_NORMAL,
                                         choices=STATUS_ITEM, verbose_name='状态')
    owner = models.ForeignKey(User, verbose_name= '作者', on_delete=None)
    created_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    objects = models.Manager()
    class Meta:
        verbose_name = verbose_name_plural = '标签'

class Post(models.Model):

    def __str__(self):
        return self.title

    @staticmethod
    def get_by_tag(tag_id):
        try:
            tag = Tag.objects.get(id=tag_id)
        except ObjectDoesNotExist:
            tag = None
            post_list = []
        else:
            post_list = tag.post_set.filter(status=Post.STATUS_NORMAL).select_related('owner', 'category')
        return post_list, tag

    @staticmethod
    def get_by_category(category_id):
        try:
            category = Category.objects.get(id=category_id)
        except ObjectDoesNotExist:
            category = None
            post_list = []
        else:
            post_list = category.post_set.filter(status=Post.STATUS_NORMAL).select_related('owner', 'category')
        return post_list, category

    @classmethod
    def latest_posts(cls):
        queryset = cls.objects.filter(status=cls.STATUS_NORMAL)
        return queryset

    @classmethod
    def hot_posts(cls):
        return cls.objects.filter(status=cls.STATUS_NORMAL).order_by('-pv')

    def save(self, *args, **kwargs):
        self.content_html = mistune.markdown(self.content)
        super().save(*args, **kwargs)

    STATUS_NORMAL = 1
    STATUS_DELETE = 0
    STATUS_DRAFT = 2
    STATUS_ITEM = (
        (STATUS_NORMAL, '正常'),
        (STATUS_DELETE, '删除'),
        (STATUS_DRAFT, '草稿')
    )

    title = models.CharField(max_length=255, verbose_name='标题')
    desc = models.CharField(max_length=1024, blank=True, verbose_name='摘要')
    content = models.TextField(verbose_name='正文', help_text='正文必须为MarkDown模式')
    content_html = models.TextField(verbose_name='正文HTML代码', blank=True,editable=False)
    status = models.PositiveIntegerField(default=STATUS_NORMAL,
                                         choices=STATUS_ITEM, verbose_name='状态')
    category = models.ForeignKey(Category, verbose_name='分类', on_delete=None)
    tag = models.ManyToManyField(Tag, verbose_name='标签')
    owner = models.ForeignKey(User, verbose_name='作者', on_delete=None)
    created_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    pv = models.PositiveIntegerField(default=1)
    uv = models.PositiveIntegerField(default=1)
    objects = models.Manager()

    class Meta:
        verbose_name = verbose_name_plural = '文章'
        ordering = ['-id']




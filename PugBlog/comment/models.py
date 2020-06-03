from django.db import models
from blog.models import Post
import re
# Create your models here.

class Comment(models.Model):
    STATUS_NORMAL = 1
    STATUS_DELETE = 0
    STATUS_ITEM = (
        (STATUS_NORMAL, '正常'),
        (STATUS_DELETE, '删除'),
    )
    target = models.CharField(max_length=100, verbose_name='评论目标')
    content = models.CharField(max_length=1000, verbose_name='内容')
    nickname = models.CharField(max_length=50, verbose_name='昵称')
    website = models.URLField(verbose_name='网站')
    email = models.EmailField(verbose_name='邮箱')
    status = models.PositiveIntegerField(default=STATUS_NORMAL, choices=STATUS_ITEM,
                                         verbose_name='状态')
    created_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    objects = models.Manager()

    @classmethod
    def get_by_target(cls, target):
        return cls.objects.filter(target=target, status=cls.STATUS_NORMAL)

    # @property
    # def get_target_title(self):
    #     pattern = re.compile(r'([0-9]+)', re.I)
    #     post_id = pattern.match(self.target, 6).group(0)
    #     post_title = Post.objects.filter(id=post_id)
    #     return post_title


    class Meta:
        verbose_name = verbose_name_plural = '评论'
        ordering = ['-id']


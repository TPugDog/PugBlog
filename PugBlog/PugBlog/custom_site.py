from  django.contrib.admin import AdminSite

class CustomSite(AdminSite):
    site_header = 'PugBlog'
    site_title = 'PugBlog 管理后台'
    index_title = '首页'

custom_site = CustomSite(name='xadmin')


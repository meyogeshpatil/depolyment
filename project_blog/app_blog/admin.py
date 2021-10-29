from django.contrib import admin
from app_blog.models import Post,comment
# Register your models here.


class admin_dislay(admin.ModelAdmin):
    list_display=['title','slug','author','body','publish','update','status']
    prepopulated_fields={'slug':('title',)}
    list_filter=('author','publish')
    search_fields=('title','body')
    raw_id_fields=('author',)
    date_hierarchy='publish'
    ordering=['status','publish']



admin.site.register(Post,admin_dislay)

class admin_comments(admin.ModelAdmin):
    list_display=['name','email','body','post','created','updated','active']
    list_filter=('active','created','updated')
    search_fields=('name','email','body')

admin.site.register(comment,admin_comments)
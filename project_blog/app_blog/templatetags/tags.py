from app_blog.models import Post
from django import template
from django.db.models import Count
register=template.Library()

@register.simple_tag(name='my_tag')
def counts():
    return Post.objects.count()

@register.inclusion_tag('app_blog/inclusion.html')
def latest_blogs(count=3):
    latest=Post.objects.order_by('-publish')[:count]
    return{'latest':latest}      

@register.inclusion_tag('app_blog/comment.html')
def most_commented(count=3):
    comment=Post.objects.annotate(total_comments=Count('comments')).order_by('-total_comments')[:count]
    return {'comment':comment}
    

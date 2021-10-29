from django.db import models
from django.contrib.auth.models import User
from django.db.models.deletion import CASCADE
from django.db.models.fields import TextField
from django.forms import widgets
from django.utils import timezone
from django.urls import reverse
from taggit.managers import TaggableManager

# Create your models here.

class custommanagers(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status='Published')

class Post(models.Model):
    status_choices=(('draft',"Draft"),('published','Published'))
    title=models.CharField(max_length=300)
    slug=models.SlugField(max_length=300,unique_for_date='publish')
    author=models.ForeignKey(User,related_name='blog_posts',on_delete=CASCADE)
    body=models.TextField()
    publish=models.DateTimeField(default=timezone.now)
    update=models.DateTimeField(auto_now=True)
    status=models.CharField(max_length=10,choices=status_choices,default='draft')
    objects=custommanagers()
    tags=TaggableManager()

    class Meta:
        ordering=('-publish',)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("post_detail", args=[self.publish.year,self.publish.strftime('%m'),self.publish.strftime('%d'),self.slug])
'''
    def get_absolute_url(self):
        return reverse("blog_by_tag_name", args=[])
   ''' 

class comment(models.Model):
    post=models.ForeignKey(Post,related_name='comments',on_delete=CASCADE)
    name=models.CharField(max_length=50)
    email=models.EmailField()
    body=models.TextField()
    created=models.DateTimeField(auto_now_add=True)
    updated=models.DateTimeField(auto_now=True)
    active=models.BooleanField(default=True)
    class Meta:
        ordering=('-created',)
    def __str__(self):
        return 'commented By {} on {}'.format(self.name,self.post)


    
    



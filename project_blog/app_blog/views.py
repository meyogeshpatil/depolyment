from typing import Coroutine
from django.shortcuts import render,get_object_or_404
from app_blog.models import Post,comment
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.core.mail import send_mail
from app_blog.forms import share_blog,comments_blog
from taggit.models import Tag

# Create your views here.
def blog(request,tag_slug=None):
    display=Post.objects.all()
    tag=None
    if tag_slug:
        tag=get_object_or_404(Tag,slug=tag_slug)
        display=display.filter(tags__in=[tag])
    paginator=Paginator(display,3)
    page_number=request.GET.get('page')
    try:
        display=paginator.page((page_number))
    except PageNotAnInteger:
        display=paginator.page(1)
    except EmptyPage:
        display=paginator.page(paginator.num_pages)
    return render(request ,'app_blog/display.html',{'display':display,'tag':tag})

def blog_detailedview(request,year,month,day,post):
    post01=get_object_or_404(Post,slug=post,status='published',publish__year=year,publish__month=month,publish__day=day)

    comments=post01.comments.filter(active=True)
    csubmit=False
    if request.method=='POST':
        form=comments_blog(request.POST)
        if form.is_valid(): 
            new_comment=form.save(commit=False)
            new_comment.post=post01
            new_comment.save()
            csubmit=True
    else:   
            form=comments_blog()         
    return render(request,'app_blog/detailed.html',{'post':post01,'form':form,'csubmit':csubmit,'comments':comments}) 

def email_func(request,id):
    post=get_object_or_404(Post,id=id,status='published')
    sent=False
    if request.method=='POST':
        form=share_blog(request.POST)
        if form.is_valid():
            cd=form.cleaned_data
            subject='{}({}) recommends you to read "{}".'.format(cd['name'],cd['email'],post.title)
            post_url=request.build_absolute_uri(post.get_absolute_url())
            message="Read Blog at:\n{}\n\n{}'s Comments:\n{}".format(post_url,cd['name'],cd['comments'])
            send_mail(subject,message,"Yogesh's Blog",[cd['to']],fail_silently=False)
            sent=True
    else:
        form=share_blog()
    return render(request,'app_blog/sendmail.html',{'form':form,'post':post,'sent':sent})

 
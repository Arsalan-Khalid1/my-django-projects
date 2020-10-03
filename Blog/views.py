from django.shortcuts import render, redirect
from Blog.models import Post, BlogComment
from Blog.templatetags import get_dict
# Create your views here.


def blogHome(request):
    allPosts = Post.objects.all()
    context = {'allPosts': allPosts}
    return render(request, 'Blog/blogHome.html', context)


def blogPost(request, slug):
    post = Post.objects.filter(slug=slug).first()
    comments = BlogComment.objects.filter(post=post, parent=None)
    replies = BlogComment.objects.filter(post=post).exclude(parent=None)
    repDict = {}
    for reply in replies:
        if reply.parent.sno not in repDict.keys():
            repDict[reply.parent.sno] = [reply]
        else:
            repDict[reply.parent.sno].append(reply)
    context = {'post': post, 'comments': comments,
               'user': request.user, 'repDict': repDict}
    return render(request, 'Blog/blogPost.html', context)


def postComments(request):
    if request.method == 'POST':
        comment = request.POST.get('comment')
        user = request.user
        postSno = request.POST.get('postSno')
        post = Post.objects.get(sno=postSno)
        parentsno = request.POST.get('parentsno')
        if parentsno == "":
            blogcomment = BlogComment(comment=comment, user=user, post=post)
        else:
            parent = BlogComment.objects.get(sno=parentsno)
            blogcomment = BlogComment(
                comment=comment, user=user, post=post, parent=parent)
        blogcomment.save()
    return redirect(f'/blog/{post.slug}')

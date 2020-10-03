from django.shortcuts import render, HttpResponse, redirect
from home.models import Contact
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from Blog.models import Post
# Create your views here.


def home(request):
    return render(request, 'home/home.html')


def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        desc = request.POST.get('desc')
        if len(name) < 2 or len(email) < 3 or len(phone) < 10 or len(desc) < 4:
            messages.error(request, "Please fill the form correctly")
        else:
            contact = Contact(name=name, email=email, phone=phone, desc=desc)
            contact.save()
            messages.success(
                request, "Your message has been successfully sent")

    return render(request, 'home/contact.html')


def about(request):
    return render(request, 'home/about.html')


def search(request):
    query = request.GET['query']
    if len(query) > 70:
        allPosts = Post.objects.none()
    else:
        allPostsTitle = Post.objects.filter(title__icontains=query)
        allPostsContent = Post.objects.filter(content__icontains=query)
        allPosts = allPostsTitle.union(allPostsContent)
    if allPosts.count() == 0:
        messages.warning(
            request, "No search results found, please refine your query")
    params = {"allPosts": allPosts, "query": query}
    return render(request, 'home/search.html', params)


def handleSignup(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        fname = request.POST.get('fname')
        lname = request.POST.get('lname')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        if len(username) > 13:
            messages.error(request, 'Username must be under 13 character')
            return redirect('home')
        if password1 != password2:
            messages.error(request, 'Passwords do not match')
            return redirect('home')
        user = User.objects.create_user(username, email, password1)
        user.first_name = fname
        user.last_name = lname
        user.save()
        messages.success(
            request, 'Your iNerd account has been created successfully')
        return redirect('home')
    else:
        return HttpResponse('404 - not found')


def handleLogin(request):
    if request.method == 'POST':
        loginusername = request.POST.get('loginusername')
        loginpass = request.POST.get('loginpass')
        user = authenticate(username=loginusername, password=loginpass)
        if user is not None:
            login(request, user)
            messages.success(request, 'Successfully logged in')
            return redirect('home')
        else:
            messages.error(request, 'Invalid cradentials, please try again')
            return redirect('home')

    else:
        return HttpResponse('404 - not found')


def handleLogout(request):
    logout(request)
    messages.success(request, "You're Logged out")
    return redirect('home')


def addPost(request):
    if request.method == 'POST':
        title = request.POST.get('postTitle')
        author = request.POST.get('postAuthor')
        slug = request.POST.get('postSlug')
        content = request.POST.get('postContent')
        post = Post(title=title, author=author, slug=slug, content=content)
        post.save()
        return redirect('home')
    count = Post.objects.count() + 1
    context = {'count': count}
    return render(request, 'home/addPost.html', context)

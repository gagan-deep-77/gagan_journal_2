from django.shortcuts import render,redirect
from django.contrib import messages,sessions
from django.http import HttpResponse

from .models import User,Post,Comment

def home(request):
    if request.session["username"]:


        context = {
            "users":User.objects.all(),
            "posts":Post.objects.all().order_by("-pub_date"),
            "not_logged_in":False,
            "current_user":request.session["username"]

        }
        return render(request,"social_app/home.html",context)
    else:
        return redirect("register")


def register(request):
    if request.session["username"]:
        return redirect("/")
    if request.method == "POST":
        username = request.POST.get("name")
        password = request.POST.get("password")
        email = request.POST.get("email")
        if User.objects.filter(name=username):
            
            messages.error(request,'A user with same name exists! login instead?')
            return render(request,"social_app/register.html")
        else:
            new_user = User.objects.create(name=username, password=password,email=email)
            new_user.save()
            request.session["username"] = username
            return redirect("home")
    return render(request,"social_app/register.html")

def login(request):
    if request.session["username"]:
        return redirect("/")
    if request.method == "POST":
        username = request.POST.get("name")
        password = request.POST.get("password")
        if not User.objects.filter(name=username):
            messages.error(request,"user does not exist, maybe you want to register?")
            return render(request,"social_app/login.html")
        else:
            user_password = User.objects.filter(name=username).first().password
            if user_password != password:
                messages.error(request,"the password does not match!")
                return render(request,"social_app/login.html")
            else:
                request.session["username"] = username
                return redirect("/")
    else:
        return render(request,"social_app/login.html")

def logout(request):
    request.session["username"] = None
    return redirect("register")


def add_post(request):
    if request.method == "POST":
        username = request.session["username"]
        user = User.objects.filter(name=username).first()
        title = request.POST.get("title")
        body = request.POST.get("body")
        new_post = Post.objects.create(user=user, title=title, body=body)
        new_post.save()
        return redirect("/")
    else:
        return render(request,"social_app/add_post.html")
    



        

def viewPost(request,id):
    user = request.session["username"]
    if request.method == "POST":
        comment_body = request.POST.get("body")
        post = Post.objects.filter(id=id).first()
        user = request.session["username"]
        user_obj = User.objects.filter(name=user).first()
        new_comment = Comment.objects.create(body=comment_body,user=user_obj,post=post)
        new_comment.save()
        return redirect("/viewPost/{}".format(id))
    post_id = id
    post = Post.objects.filter(id=post_id).first()
    comments = Comment.objects.filter(post=post)
    context = {
        'current_user':user,
        "post":post,
        "comments":comments,
    }
    return render(request,"social_app/view_post.html",context)


def viewUser(request,id):
    user = User.objects.filter(id=id).first()
    posts = Post.objects.filter(user=user)
    context = {
        "user":user,
        "posts":posts
    }
    return render(request,"social_app/view_user.html",context)

def deletePost(request,id):
    post = Post.objects.filter(id=id).first()
    post.delete()
    return redirect("/")

def deleteComment(request,id):
    comment = Comment.objects.filter(id=id).first()
    post_id = comment.post.id
    comment.delete()
    return redirect("/viewPost/{}".format(post_id))

def editPost(request,id):
    new_post = Post.objects.filter(id=id).first()
    context = {
        "post":new_post,
    }
    if request.method == "POST":
        post_body = request.POST.get("post_body")
        post_title = request.POST.get("post_title")
        new_post.body = post_body
        new_post.title = post_title
        new_post.save()
        return redirect("/viewPost/{}".format(id))
        
    return render(request,"social_app/edit_post.html",context)
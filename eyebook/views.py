from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth.models import User,auth
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from datetime import date
from eyebook import models
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponseRedirect
from django.views.decorators.csrf import ensure_csrf_cookie,csrf_protect,csrf_exempt,requires_csrf_token


# Create your views here.
def addpost(request):
    username = request.session['username']
    res = render(request,'eyebook/addpost.html',{'username':username})
    return res

# @csrf_exempt
def like_post(request):
    # if request.is_ajax():
    #     username = request.post.get('like_username')
    #     print(username)
    #     print("working")
    # else:
    #     print("not working")

    if request.method == 'GET':
        post_id = request.GET['post_id']
        post_like_name = request.GET['post_like_name']

        l = models.Likes()

        l.post_id = post_id
        l.like_username = post_like_name

        l.save()

        print(post_id)
        print(post_like_name)


        # likedpost = Post.obejcts.get(pk=post_id) #getting the liked posts
        # m = Like(post=likedpost) # Creating Like Object
        # m.save()  # saving it to store in database
        return HttpResponse(post_id) # Sending an success response
    else:
        return HttpResponse("Request method is not a GET")

    # return HttpResponse(str("shubham"))

def mypost(request):
    username = request.session['username']
    posts=models.Posts.objects.filter(username=username).order_by('time')
    # posts=models.Posts.objects.all()
    res = render(request,'eyebook/mypost.html',{'username':username,'posts':posts})
    return res

def upload(request):
    if request.method=='POST':
        uploaded_file = request.FILES['document']
        fs=FileSystemStorage()
        fs.save(uploaded_file.name,uploaded_file)
        print(uploaded_file.name)
        print(uploaded_file.size)
        img_name=uploaded_file.name

        # res = render(request,'eyebook/addpost',{'img_name':img_name})

        return redirect('/eyebook/addpost')


def add(request):
    if request.method=='POST':

        post=models.Posts()

        usename = request.session['username']
        today = date.today()

        post_text = request.POST['post_text']

        uploaded_file = request.FILES['document']
        fs=FileSystemStorage()
        fs.save(uploaded_file.name,uploaded_file)
        print(uploaded_file.name)
        print(uploaded_file.size)

        img_name=uploaded_file.name

        # post.post_id =
        post.username = usename
        post.time = today
        post.post_text = post_text
        post.post_img = img_name

        print(post.post_id)

        post.save()

        return HttpResponseRedirect('/eyebook/mypost')

@login_required(login_url='/eyebook/login')
def home(request):
    username = request.session['username']
    posts=models.Posts.objects.all()
    likes=models.Likes.objects.all()
    res = render(request,'eyebook/home.html',{'username':username,'posts':posts,'likes':likes})
    return res

def confirm(request):
    res = render(request,'eyebook/confirmation.html')
    return res

def login_page(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username,password=password)
        if user is not None:
            auth.login(request,user)
            request.session['username'] = username
            return redirect('/eyebook/home')
        else:
            print("Invalid Credentials")
            msg = "*Invalid Credentials"
            res = render(request,'eyebook/login.html',{'msg':msg})
    else:
        res = render(request,'eyebook/login.html')
    return res

def userLogout(request):
    auth.logout(request)
    return redirect('/eyebook/login')

def sign_up_page(request):
    if request.method == 'POST':
        name=request.POST['name']
        email=request.POST['email']
        username = email.split('@')[0]
        password1=request.POST['password1']
        password2=request.POST['password2']
        if len(password1)<8:
            print("Password should be minimum 8 characters")
            msg = "*Password should be minimum 8 characters"
            res = render(request,'eyebook/sign_up.html',{'msg':msg})
        elif password1==password2:
            if User.objects.filter(username=username).exists():
                print("Email already exists")
                msg = "*Email already exists"
                res = render(request,'eyebook/sign_up.html',{'msg':msg})
            else:
                user = User.objects.create_user(username=username , password=password1 , email = email,first_name = name)
                user.save()
                print("user created")
                return redirect('/eyebook/confirmation')
                # res = render(request,'eyebook/home.html')
        else:
            print("Password not matching")
            msg = "*Password not matching"
            res = render(request,'eyebook/sign_up.html',{'msg':msg})
    else:
        res = render(request,'eyebook/sign_up.html')
    return res

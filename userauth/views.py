from itertools import chain
from  django . shortcuts  import  get_object_or_404, render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from . models import  Followers, LikePost, Post, Profile, Comments, Replies, Liked_Comments
from django.db.models import Q
from django.contrib.auth import get_user_model

User = get_user_model()



def signup(request):
 try:
    if request.method == 'POST':
        fnm=request.POST.get('fnm')
        emailid=request.POST.get('emailid')
        pwd=request.POST.get('pwd')
        print(fnm,emailid,pwd)
        my_user = User.objects.create_user(username=fnm, email=emailid, password=pwd)
        my_user.save()
        user_model = User.objects.get(username=fnm)
        new_profile = Profile.objects.create(user=user_model, id_user=user_model.id)
        new_profile.save()
        if my_user is not None:
            login(request,my_user)
            return redirect('/')
        return redirect('/loginn')
    
        
 except:
        invalid="User already exists"
        return render(request, 'signup.html',{'invalid':invalid})
  
    
 return render(request, 'signup.html')
        
     
        
        
        
        
    

def loginn(request):
 
  if request.method == 'POST':
        fnm=request.POST.get('fnm')
        pwd=request.POST.get('pwd')
        print(fnm,pwd)
        userr=authenticate(request,username=fnm,password=pwd)
        if userr is not None:
            login(request,userr)
            return redirect('/')
        
 
        invalid="Invalid Credentials"
        return render(request, 'loginn.html',{'invalid':invalid})
               
  return render(request, 'loginn.html')

@login_required(login_url='/loginn')
def logoutt(request):
    logout(request)
    return redirect('/loginn')



@login_required(login_url='/loginn')
def home(request):
    
    following_users = Followers.objects.filter(follower=request.user.username).values_list('user', flat=True)

    
    post = Post.objects.filter(Q(user=request.user.username) | Q(user__in=following_users)).order_by('-created_at')

    profile = Profile.objects.get(user=request.user)

    context = {
        'post': post,
        'profile': profile,
    }
    return render(request, 'main.html',context)
    


@login_required(login_url='/loginn')
def upload(request):

    if request.method == 'POST':
        user = request.user.username
        image = request.FILES.get('image_upload')
        caption = request.POST['caption']

        new_post = Post.objects.create(user=user, image=image, caption=caption)
        new_post.save()

        return redirect('/')
    else:
        return redirect('/')

@login_required(login_url='/loginn')
def likes(request, id):
    if request.method == 'GET':
        username = request.user.username
        post = get_object_or_404(Post, id=id)

        like_filter = LikePost.objects.filter(post_id=id, username=username).first()

        if like_filter is None:
            new_like = LikePost.objects.create(post_id=id, username=username)
            post.no_of_likes = post.no_of_likes + 1
        else:
            like_filter.delete()
            post.no_of_likes = post.no_of_likes - 1

        post.save()

        # Generate the URL for the current post's detail page
        print(post.id)

        # Redirect back to the post's detail page
        return redirect('/#'+id)
    
@login_required(login_url='/loginn')
def explore(request):
    post=Post.objects.all().order_by('-created_at')
    profile = Profile.objects.get(user=request.user)

    context={
        'post':post,
        'profile':profile
        
    }
    return render(request, 'explore.html',context)
    
@login_required(login_url='/loginn')
def profile(request,id_user):
    user_object = User.objects.get(username=id_user)
    print(user_object)
    profile = Profile.objects.get(user=request.user)
    user_profile = Profile.objects.get(user=user_object)
    user_posts = Post.objects.filter(user=id_user).order_by('-created_at')
    user_post_length = len(user_posts)

    follower = request.user.username
    user = id_user
    
    if Followers.objects.filter(follower=follower, user=user).first():
        follow_unfollow = 'Unfollow'
    else:
        follow_unfollow = 'Follow'

    user_followers = len(Followers.objects.filter(user=id_user))
    user_following = len(Followers.objects.filter(follower=id_user))

    context = {
        'user_object': user_object,
        'user_profile': user_profile,
        'user_posts': user_posts,
        'user_post_length': user_post_length,
        'profile': profile,
        'follow_unfollow':follow_unfollow,
        'user_followers': user_followers,
        'user_following': user_following,
    }
    
    
    if request.user.username == id_user:
        if request.method == 'POST':
            if request.FILES.get('image') == None:
             image = user_profile.profileimg
             bio = request.POST['bio']
             location = request.POST['location']

             user_profile.profileimg = image
             user_profile.bio = bio
             user_profile.location = location
             user_profile.save()
            if request.FILES.get('image') != None:
             image = request.FILES.get('image')
             bio = request.POST['bio']
             location = request.POST['location']

             user_profile.profileimg = image
             user_profile.bio = bio
             user_profile.location = location
             user_profile.save()
            

            return redirect('/profile/'+id_user)
        else:
            return render(request, 'profile.html', context)
    return render(request, 'profile.html', context)

@login_required(login_url='/loginn')
def delete(request, id):
    post = Post.objects.get(id=id)
    post.delete()

    return redirect('/profile/'+ request.user.username)


@login_required(login_url='/loginn')
def search_results(request):
    query = request.GET.get('q')

    users = Profile.objects.filter(user__username__icontains=query)
    posts = Post.objects.filter(caption__icontains=query)
    context = {
        'query': query,
        'users': users,
        'posts': posts,
    }
    return render(request, 'search_user.html', context)

def home_post(request,id):
    post=Post.objects.get(id=id)
    profile = Profile.objects.get(user=request.user)
    context={
        'post':post,
        'profile':profile
    }
    return render(request, 'main.html',context)



def follow(request):
    if request.method == 'POST':
        follower = request.POST['follower']
        user = request.POST['user']

        if Followers.objects.filter(follower=follower, user=user).first():
            delete_follower = Followers.objects.get(follower=follower, user=user)
            delete_follower.delete()
            return redirect('/profile/'+user)
        else:
            new_follower = Followers.objects.create(follower=follower, user=user)
            new_follower.save()
            return redirect('/profile/'+user)
    else:
        return redirect('/')
    
def comment(request, post_id):
    if request.method=='POST':
        comment=request.POST['comments']
        comment=Comments.objects.create(comments=comment,
                                        post_id=post_id,
                                        user=request.user.username)
        comment.save()
        return redirect('/')
    
def comment_show(request, id):
    comments=Comments.objects.filter(post_id=id)
    context={
        'comments':comments
    }
    return render(request, "comment.html", context)        

def comment_delete(request, comment_id):
    comment = get_object_or_404(Comments, id=comment_id)  # Ensures the comment exists
    comment.delete()
    
    # Redirect to the same post's comment section
    return redirect(request.META.get('HTTP_REFERER', '/comments/'))

def comment_editform(request, comment_id):
    comment= get_object_or_404(Comments, id=comment_id)
    context={
        'comment':comment
    }
    return render(request, "editform.html", context)
def comment_edit(request, comment_id):
    if request.method=='POST':
        new_comment=request.POST['comments']
        comment= get_object_or_404(Comments, id=comment_id)
        comment.comments=new_comment
        comment.save()
        return redirect(request.META.get('HTTP_REFERER', '/comments/'))

def show_liked_by(request, post_id):
    liked_by = LikePost.objects.filter(post_id=post_id)
    context={
        'likes':liked_by
    }
    return render(request, "liked_by.html", context)    

def show_replyform(request, comment_id):
    context={
        'comment_id':comment_id
    }
    return render(request, "reply_form.html", context)
def reply(request, comment_id):
    if request.method=='POST':
        reply=request.POST['reply']
        reply=Replies.objects.create(comment_id=comment_id,
                                     reply=reply,
                                     user=request.user.username)
        reply.save()
        return redirect(request.META.get('HTTP_REFERER', '/comments/'))

def reply_show(request, comment_id):
    replies=Replies.objects.filter(comment_id=comment_id)
    context={
        'replies':replies
    }
    return render(request, "reply.html", context)
def reply_delete(request, reply_id):
    reply= get_object_or_404(Replies, id=reply_id)
    reply.delete()
    return redirect(request.META.get('HTTP_REFERER', '/comments/'))
def like_comment(request, comment_id):  
    comment = get_object_or_404(Comments, id=comment_id)

    # Check if the user has already liked the comment
    is_liked = Liked_Comments.objects.filter(comment_id=comment_id, user=request.user.username).first()

    if is_liked:
        # Unlike: Remove the like entry and decrement like count
        is_liked.delete()
        comment.no_of_likes = max(0, comment.no_of_likes - 1)  # Ensure likes don't go negative
    else:
        # Like: Create a new like entry and increment like count
        Liked_Comments.objects.create(comment_id=comment_id, user=request.user.username)
        comment.no_of_likes += 1
    comment.save()
    return redirect(request.META.get('HTTP_REFERER', '/comments/'))
def like_comment_show(request, comment_id):
    likes=Liked_Comments.objects.filter(comment_id=comment_id)
    context={
        'likes':likes
    }
    return render(request, "comment_liked_by.html", context)

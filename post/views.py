from django.shortcuts import render,redirect,HttpResponse
from .models import Post 
from .forms import PostForm
from emailVerification.decorators import email_vrf_required
# Create your views here.

@email_vrf_required
def create_post(request):
    if request.method == 'POST':
        print('post')
        form = PostForm(request.POST,request.FILES)
        if form.is_valid():
            post=request.FILES['post']
            caption=form.cleaned_data.get('caption')
            user=request.user
            obj=Post.objects.create(user=user,post=post,caption=caption)
            obj.save()
            return redirect('home:home')  # Redirect to a page displaying all posts
    else:
        form = PostForm()
    return render(request, 'post/create_post.html', {'form': form})

@email_vrf_required
def delete_post(request):
    print('start')
    if request.method == 'POST':
        
        
        user=request.user
        post=Post.objects.filter(id=request.POST.get('post_id'))[0]
        print('post')
        post.delete()
        print('delete')
    else :
        print('else')


    return redirect('home:home')

@email_vrf_required
def like_post(request):
    user=request.user
    post_id=request.POST.get('post_id')
    post=Post.objects.filter(id=post_id)[0]
    post.likes=post.likes+1
    post.save()
    
    return redirect('home:home')

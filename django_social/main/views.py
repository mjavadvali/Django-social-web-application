from django.http import JsonResponse
from django.shortcuts import redirect, HttpResponseRedirect, get_object_or_404, render
from django.views.generic import ListView, CreateView, DetailView, DeleteView
from django.views.generic.edit import ModelFormMixin
from .forms import PostForm, CommentForm
from.models import Post, Like, Comment, Bookmark
from django.urls import reverse_lazy, reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.decorators.cache import cache_page
from account.models import User
from django.utils.text import slugify
import random
from django.contrib.auth.decorators import login_required


class ListPost(LoginRequiredMixin, ListView):
    success_url = reverse_lazy('main:listview')
    template_name = 'post/postlist.html'
    context_object_name = 'posts'
    
    def get_queryset(self):
        return Post.objects.order_by('-created')
    
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user
        return context
    

def tag_users(request):
    if request.method == "POST":
        tagged_users = request.POST.getlist('tagged_users')
        print('users')
        print(request.POST.getlist('tagged_users'))
        print(request.POST.get('tagged_users'))
        
        request.session['tagged_users'] = tagged_users
        print('this is session:',request.session['tagged_users'] )
        return HttpResponseRedirect(request.GET.get('next', '/'))
    
    users = User.objects.all()
    return render(request, 'post/tag_users.html', {'users': users})

class PostDetail(ModelFormMixin, DetailView):
    template_name = 'post/post_detail.html'
    model = Post
    form_class = CommentForm
    context_object_name = 'post'

    def get_object(self):
        return get_object_or_404(Post, slug=self.kwargs['slug'])

    def get(self, request, *args, **kwargs):
        post = self.get_object()
        form = CommentForm(post=post)
        comments = Comment.objects.filter(post=post)
        return render(request, self.template_name, {'form': form, 'post': post, 'comments': comments})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = self.get_object()
        context['comments'] = Comment.objects.filter(post=post)
        context['form'] = self.form_class
        return context
    # def get_form(self, form_class=None):
    #     post = self.get_object()
    #     return self.form_class(post=post)


def handle_like(request, slug):
    post = get_object_or_404(Post, slug=slug)
    user = request.user

    like, created = Like.objects.get_or_create(user=user, post=post)
    if like:
        if like.value == 'Like':
            post.likes.add(user)
            like.value = 'Unlike'
            
        else:
            post.likes.remove(user)
            like.value = 'Like'
        
        post.save()
        like.save()
            
    if created:
        post.likes.add(user)
        like.value = 'Unlike'
        
        post.save()
        like.save()

    next_url = request.GET.get('next')

    if next_url:
        return redirect(next_url)
    return redirect('main:listview')



def handle_comment(request, slug, parent_id=None):
    post = Post.objects.get(slug=slug)
    user = request.user
    form = CommentForm(post=post)
    print('comments')
    print(Comment.objects.filter(post=post))
    if request.method == 'POST':
        form = CommentForm(request.POST, post=post)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = user
            comment.post = post
            if parent_id:
                parent = Comment.objects.get(pk= parent_id)
                comment.parent = parent
                comment.save()
            comment.save()
            return redirect('main:post_detail', slug=post.slug)
        else:
            print(form.errors)
    return redirect(request, 'post/post_detail.html', {'form': form})


def search_view(request):
    query = request.GET.get('q', '')
    users = User.objects.filter(username__icontains=query).exclude(username= request.user.username)
    data = [{'username': user.username, 'url': user.get_absolute_url()} for user in users]
    return JsonResponse(data, safe=False)

        
def post_delete(request, slug):
    post = get_object_or_404(Post, slug=slug)
    post.delete()
    return redirect('dashboard')
    

def bookmark_post(request, slug):
    post = get_object_or_404(Post, slug=slug)
    user = request.user

    bookmark, created = Bookmark.objects.get_or_create(user=user, post=post)
    if bookmark:
        if bookmark.value == 'Save':
            post.bookmarks.add(user)
            bookmark.value = 'Unsave'
            
        else:
            post.bookmarks.remove(user)
            bookmark.value = 'Save'
        
        post.save()
        bookmark.save()
            
    if created:
        post.bookmarks.add(user)
        bookmark.value = 'Unsave'
        
        post.save()
        bookmark.save()


    current_path = request.path
    if current_path == '/':
        return redirect('main:listview')
    return redirect('main:post_detail', slug=post.slug)


@login_required
def create_post(request):
    form = PostForm()
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            slug = slugify(post.title)
            while Post.objects.filter(slug=slug).exists():
                random_number = random.random()
                slug += str(random_number)
            post.slug = slug
            try:
                post.save()
                print('the form is sent correrctly')
                return redirect('main:listview')
            except PermissionError:
                print('errors occured')
                return render(request, 'post/create_post.html', {'form': form})

    return render(request, 'post/create_post.html', {'form': form})
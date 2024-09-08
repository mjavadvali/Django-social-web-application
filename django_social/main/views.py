from django.http import JsonResponse
from django.shortcuts import redirect, HttpResponseRedirect, get_object_or_404, render
from django.views.generic import ListView, CreateView, DetailView, DeleteView
from django.views.generic.edit import ModelFormMixin
from .forms import PostForm, CommentForm
from.models import Post, Like, Comment, Bookmark
from django.urls import reverse_lazy, reverse
from django.contrib.auth.mixins import LoginRequiredMixin
import json
from account.models import User


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
    
class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'post/create_post.html'
    success_url = reverse_lazy('main:listview')
    

    def get_form(self, form_class=form_class):
        form = super().get_form(form_class)
        return form
    


    def form_valid(self, form):
        
        post = form.save(commit=False)      
        post.user = self.request.user
        tagged_user_ids = self.request.session.get('tagged_users', [])
        print('these are tag users: ',tagged_user_ids)
        tagged_users = User.objects.filter(id__in=tagged_user_ids)
        post.tagged_users.set(tagged_users)
        post.save()

        self.request.user.posts += 1
        self.request.user.save()
        return super().form_valid(form)

    def form_invalid(self, form):
        print(form.errors)
        return super().form_invalid(form)

def tag_users(request):
    if request.method == "POST":
        tagged_users = request.POST.getlist('tagged_users')
        request.session['tagged_users'] = tagged_users
        print('this is session:',request.session['tagged_users'] )
        return HttpResponseRedirect(request.GET.get('next', '/'))
    
    users = User.objects.all()
    return render(request, 'post/tag_users.html', {'users': users})

class PostDetail(ModelFormMixin, DetailView):
    template_name = 'post\post_detail.html'
    model = Post
    form_class = CommentForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = self.get_object()
        context['comments'] = Comment.objects.filter(post=post)
        context['form'] = self.form_class
        return context



def handle_like(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
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

    return redirect('main:listview')


def handle_comment(request, post_id, parent_id=None):
    post = Post.objects.get(pk=post_id)
    user = request.user
    form = CommentForm()
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = user
            comment.post = post
            if parent_id:
                parent = Comment.objects.get(pk= parent_id)
                comment.parent = parent
                comment.save()
            comment.save()
            return redirect('main:post_detail', pk=post.id)
        else:
            print(form.errors)
    return redirect('main:post_detail', pk=post.id)




def search_view(request):


    query = request.GET.get('q', '')
    users = User.objects.filter(username__icontains=query).exclude(username= request.user.username)
    data = [{'username': user.username, 'url': user.get_absolute_url()} for user in users]
    return JsonResponse(data, safe=False)

        
    # return JsonResponse({'error': 'Bad request'}, status=400)


# class Temp(LoginRequiredMixin, ListView):
    
#     success_url = reverse_lazy('main:temp')
#     template_name = 'post/temp.html'
#     context_object_name = 'posts'
    
#     def get_queryset(self):
#         return Post.objects.order_by('-created')
    
    
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['user'] = self.request.user
#         return context
    

def post_delete(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    post.delete()
    
    # return redirect(request.META.get('HTTP_REFERER'))
    return redirect('dashboard')
    

def bookmark_post(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
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

    return redirect('main:listview')


    
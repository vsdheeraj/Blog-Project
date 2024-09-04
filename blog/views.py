from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.urls import reverse_lazy

from .models import Post,Comment
from .forms import PostForm,CommentForm

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin    # for class based
from django.views.generic import (TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView)

# Create your views here.

class AboutView(TemplateView):
    template_name = "about.html"
    
class PostListView(ListView):
    model = Post
    
    def get_queryset(self):           # defining how i want to grab that list. And this allows me to use Django's ORM when dealing with just generic views that way I can add a lil more of a custom touch to it. 
        return Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')  # __lte = less than or equal to, -published_date = in decending order
    
class PostDetailView(DetailView):
    model = Post

class PostCreateView(LoginRequiredMixin, CreateView):
    login_url = '/login/'              # incase the person is not logged in.
    redirect_field_name = 'blog/post_detail.html'
    form_class = PostForm
    model = Post
    
class PostUpdateView(LoginRequiredMixin,UpdateView):
    login_url = '/login/'
    redirect_field_name = 'blog/post_detail.html'
    form_class = PostForm
    model = Post

class PostDeleteView(LoginRequiredMixin,DeleteView):
    model = Post
    success_url = reverse_lazy('post_list') # we don't want the success_url to actually activate until we delete it. Otherwise we jump into someother page.
    
class DraftListView(LoginRequiredMixin,ListView):
    login_url = '/login/'
    redirect_field_name = 'blog/post_list.html'
    model = Post
    
    def get_queryset(self):
        return Post.objects.filter(published_date__isnull=True).order_by('created_date')

#######################################
## Functions that require a pk match ##
#######################################

@login_required
def post_publish(request,pk):
    post = get_object_or_404(Post,pk=pk)
    post.publish()
    return redirect('post_detail',pk=pk)

@login_required
def add_comment_to_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = CommentForm()
    return render(request, 'blog/comment_form.html', {'form': form})


@login_required    
def comment_approve(request,pk):
    comment = get_object_or_404(Comment,pk=pk)
    comment.approve()
    return redirect('post_detail',pk=comment.post.pk)

@login_required
def comment_remove(request,pk):
    comment = get_object_or_404(Comment,pk=pk)
    post_pk = comment.post.pk                  # after delete by the time u get to return, it's not gonna remember wt's that post.pk was, which is y we need to save it as an extra variable before we delete it.
    comment.delete()
    return redirect('post_detail', pk=post_pk)
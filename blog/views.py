from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from .models import Post, Comment
from .forms import CommentForm
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin


def home(request):
    post_list = Post.objects.all().order_by('-date_posted')
    paginator = Paginator(post_list, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'blog/home.html', {'page_obj': page_obj})


def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    comments = post.comments.order_by('-date_posted')
    if request.method == 'POST':
        if not request.user.is_authenticated:
            return redirect('login')
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            return redirect('post-detail', pk=post.pk)
    else:
        form = CommentForm()

    context = {
        'post': post,
        'comments': comments,
        'form': form,
    }
    return render(request, 'blog/post_detail.html', context)


class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post_detail.html'
    context_object_name = 'post'


def about(request):
    return render(request, 'blog/about.html', {'title': 'About'})


class UserPostListView(ListView):
    model = Post
    template_name = 'blog/user_posts.html'
    context_object_name = 'posts'
    paginate_by = 5

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_posted')


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content']
    template_name = 'blog/post_form.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content']
    template_name = 'blog/post_form.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    template_name = 'blog/post_confirm_delete.html'
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author
    
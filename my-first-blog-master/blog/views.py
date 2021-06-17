from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from .models import Post, Comment
from .forms import PostForm, CommentForm
from django.contrib.auth.decorators import login_required

# Create your views here.
def post_list(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date') # query set
    return render(request, 'blog/post_list.html', {'posts':posts})

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'blog/post_detail.html', {'post': post})

@login_required
def post_new(request):
    if request.method == "POST": # 폼에 데이터를 입력한 경우
        form = PostForm(request.POST) # 폼에서 받은 데이터 가져오기
        if form.is_valid():
            post = form.save(commit=False) # 받은 데이터를 바로 Post모델에 저장하지 말기
            post.author = request.user # author 추가
            #post.published_date = timezone.now() # publish_date 현재시간으로 추가
            post.save() # 변경사항 저장
            return redirect('post_detail', pk=post.pk) # 저장 후 post_detail 뷰로 이동
    else: # 처음 페이지 접속
        form = PostForm() # 비어있는 폼 제공
    return render(request, 'blog/post_edit.html', {'form':form})

@login_required
def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk) # Post 모델 가져오기
    if request.method == "POST": # 수정된 글을 입력한 경우
        form = PostForm(request.POST, instance=post) # 수정된 데이터를 가져오기
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else: # 글을 수정하려고 처음 버튼을 눌렀을 때
        form = PostForm(instance=post) # 작성되었던 글을 불러오는 것
    return render(request, 'blog/post_edit.html', {'form': form})

# 임시저장(draft)
@login_required
def post_draft_list(request):
    posts = Post.objects.filter(published_date__isnull=True).order_by('created_date') # 발행되지 않은 글 목록 가져오기
    return render(request, 'blog/post_draft_list.html', {'posts': posts})

@login_required
def post_publish(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.publish()
    return redirect('post_detail', pk=pk)

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
    return render(request, 'blog/add_comment_to_post.html', {'form': form})

@login_required
def comment_approve(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.approve()
    return redirect('post_detail', pk=comment.post.pk)

@login_required
def comment_remove(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.delete()
    return redirect('post_detail', pk=comment.post.pk)
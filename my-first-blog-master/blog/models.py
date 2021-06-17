from django.db import models
from django.conf import settings
from django.utils import timezone

# 모델(객체) 정의
class Post(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE) # 다른 모델에 대한 링크
    title = models.CharField(max_length=200) # 글자수가 제한된 텍스트
    text = models.TextField() # 글자수에 제한이 없는 긴 텍스트
    created_date = models.DateTimeField(default=timezone.now) # 날짜와 시간
    published_date = models.DateTimeField(blank=True, null=True)

    # Post 모델의 날짜와 시간을 알려주는 메소드
    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def approved_comments(self):
        return self.comments.filter(approved_comment=True)

    # Post 모델의 제목을 알려주는 메소드
    def __str__(self):
        return self.title

class Comment(models.Model):
    post = models.ForeignKey('blog.Post', on_delete=models.CASCADE, related_name='comments') #related_name 옵션을 통해 Post 모델에서 댓글에 access하게 함
    author = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    approved_comment = models.BooleanField(default=False)

    def approve(self):
        self.approved_comment = True
        self.save()

    def __str__(self):
        return self.text

from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from PIL import Image 


class Profile(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    image=models.ImageField(default='profile_pics/default.jpg',upload_to='profile_pics')

    def __str__(self):
        return f'{self.user.username} Profile'  

class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk': self.pk} )


class Comment(models.Model):
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'Comment by {self.author.username} on {self.post.title}'

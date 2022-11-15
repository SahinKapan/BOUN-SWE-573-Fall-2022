from django.db import models
from django.urls import reverse_lazy
from django.conf import settings

import misaka

from discussiongroups.models import DiscussionGroup

# Create your models here.

from django.contrib.auth import get_user_model
User = get_user_model()

class Post(models.Model):
    user = models.ForeignKey(User,related_name='posts')
    created_at = models.DateTimeField(auto_now=True)
    message = models.TextField()
    message_html = models.TextField(editable=False)
    discussiongroup = models.ForeignKey(DiscussionGroup,related_name='posts',null=True,blank=True)

    def __str__(self):
        return self.message

    
    def save(self,*args,**kwargs):
        self.message_html = misaka.html(self.message)
        super().save(*args,**kwargs)

    def get_absolute_url(self):
        return reverse_lazy('posts:single',kwargs={'username':self.user.username,
                                               'pk':self.pk})

    class Meta:
        ordering = ['-created_at']
        unique_together = ['user','message']
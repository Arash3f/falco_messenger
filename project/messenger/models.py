from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify

class GroupChat(models.Model):
    name    = models.CharField(max_length =20)
    slug    = models.SlugField(unique=True, allow_unicode=True, max_length=255)
    creator = models.ForeignKey(User , on_delete=models.CASCADE)
    image   = models.ImageField(upload_to="group_image/" , null=True , blank = True)
    date_create = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        unique_together = ['slug', 'name']

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(GroupChat, self).save(*args, **kwargs)
        
class Members(models.Model):
    date_join = models.DateTimeField(auto_now=True)
    chat      = models.ForeignKey(GroupChat , on_delete=models.CASCADE , related_name="members")
    user      = models.ForeignKey(User ,on_delete=models.CASCADE , related_name="members")

    def __str__(self):
        return self.user.username

class Message(models.Model):
    chat    = models.ForeignKey(GroupChat , on_delete=models.CASCADE , related_name="messages")
    author  = models.ForeignKey(User ,on_delete=models.CASCADE)
    body    = models.TextField()
    warning = models.BooleanField(default=False)
    date_create = models.DateTimeField(auto_now=True)

    def join(self):
        return f"User {self.author.username} Joined chat :)"

    def create(self):
        return f"User {self.author.username} Create Group :)"
        
    def leave(self):
        return f"User {self.author.username} leave chat :("

    def kick(self):
        return f"User {self.author.username} kicked :("

    def __str__(self):
        return self.author.username

    def date_format(self):
        return str(self.date_create.strftime("%Y-%m-%d %I:%M %p"))
from django.db import models
from django.utils import timezone
from django.urls import reverse

# Create your models here.
class Post(models.Model):
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    title = models.CharField(max_length=256)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)     # That exact date&time when submitted will be noted.
    published_date = models.DateTimeField(blank=True, null=True)   # null=True pertains to the database schema, allowing for NULL values in the database, while blank=True is related to form validation, enabling fields to be left empty in form submissions 
    
    def publish(self):
        self.published_date = timezone.now()    # when clicked on publish that exact date&time when submitted will be noted.
        self.save()
        
    def approve_comments(self):
        return self.comments.filter(approved_comment=True)   # filtering comments that are approved
    
    def get_absolute_url(self):
        return reverse("post_detail", kwargs={"pk": self.pk})  # once u submitted the post, this method will take you that post detail page for the primary key you just created.
    
    def __str__(self):
        return self.title 
    
class Comment(models.Model):
    post = models.ForeignKey("blog.Post", related_name='comments', on_delete=models.CASCADE) # it's going to connect each comment to an actual post.
    author = models.CharField(max_length=256)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    approved_comment = models.BooleanField(default=False)  # default=False coz haven't approved this comment yet.
    # approved_comment must be same as mentioned in method-approve_comments under class-Post.
    
    def approve(self):
        self.approved_comment = True
        self.save()
    
    def get_absolute_url(self):   # it will tell django to where to go back after submitting.
        return reverse("post_list") # after a comment is approved by a superuser, it will take back to post lists
    
    def __str__(self):
        return self.text
from django.db import models
from nomadgram.users import models as user_models
from django.utils.encoding import python_2_unicode_compatible
# Create your models here.

@python_2_unicode_compatible
class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now=True)

    #abstract base Model
    #This model will not be used to create any database table.
    class Meta:
        abstract = True

@python_2_unicode_compatible
class Image(TimeStampedModel):
    
    """ Image Model """        
    file = models.ImageField()
    location = models.CharField(max_length=140)
    caption = models.TextField()
    creator = models.ForeignKey(user_models.User, null = True, on_delete=models.CASCADE, related_name='images')   

    @property
    def like_count(self):
        return self.likes.all().count()

        
    @property
    def comment_count(self):
        return self.comments.all().count()
    

    #string representation
    def __str__(self):
        return '{} - {}'.format(self.location, self.caption)
    
    # for models's setting
    class Meta:
        ordering = ['-created_at']

@python_2_unicode_compatible
class Comment(TimeStampedModel):

    """ Comment Model """
    message = models.TextField()
    creator = models.ForeignKey(user_models.User, null = True,on_delete=models.CASCADE)
    image = models.ForeignKey(Image, null = True,on_delete=models.CASCADE, related_name = 'comments')

    #string representation
    def __str__(self):
        return self.message

@python_2_unicode_compatible
class Like(TimeStampedModel):
    
    """ Like Model """
    creator = models.ForeignKey(user_models.User, null = True,on_delete=models.CASCADE)
    image = models.ForeignKey(Image, null = True,on_delete=models.CASCADE, related_name = 'likes')

    #string representation
    def __str__(self):
        return 'User_name : {} - Image_caption : {}'.format(self.creator.username, self.image.caption)
    

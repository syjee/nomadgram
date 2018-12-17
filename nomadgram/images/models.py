from django.db import models
from nomadgram.users import models as user_models

# Create your models here.

class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now=True)

    #abstract base Model
    #This model will not be used to create any database table.
    class Meta:
        abstract = True


class Image(TimeStampedModel):
    
    """ Image Model """        
    file = models.ImageField()
    location = models.CharField(max_length=140)
    caption = models.TextField()
    creator = models.ForeignKey(user_models.User, null = True, on_delete=models.CASCADE)   


class Comment(TimeStampedModel):

    """ Comment Model """
    message = models.TextField()
    creator = models.ForeignKey(user_models.User, null = True,on_delete=models.CASCADE)
    image = models.ForeignKey(Image, null = True,on_delete=models.CASCADE)

class Like(TimeStampedModel):
    
    """ Like Model """
    creator = models.ForeignKey(user_models.User, null = True,on_delete=models.CASCADE)
    image = models.ForeignKey(Image, null = True,on_delete=models.CASCADE)

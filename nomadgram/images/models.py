from django.db import models

# Create your models here.

class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now=True)

    #abstract base Model
    #This model will not be used to create any database table.
    class Meta:
        abstract = True


class Images(TimeStampedModel):
    
    file = models.ImageField()
    location = models.CharField(max_length=140)
    caption = models.TextField()


class Comment(TimeStampedModel):

    message = models.TextField()

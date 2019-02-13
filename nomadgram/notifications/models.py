from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from nomadgram.users import models as user_models 
from nomadgram.images import models as image_models

class Notification(image_models.TimeStampedModel):

    TYPE_CHOICES = (
        #('for DB', 'for admin_pannel')
        ('follow','Follow'),
        ('like','Like'),
        ('comment','Comment')
    )

    creator = models.ForeignKey(user_models.User, on_delete=models.CASCADE,related_name = 'creator')
    to = models.ForeignKey(user_models.User, on_delete=models.CASCADE,related_name = 'to')
    
    notification_type = models.CharField(max_length=20, choices = TYPE_CHOICES)
    image = models.ForeignKey(image_models.Image,on_delete=models.CASCADE, null=True, blank=True)

    comment = models.TextField(null=True, blank = True)
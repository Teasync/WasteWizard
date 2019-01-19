from django.db import models


class Item(models.Model):
    body = models.TextField()
    category = models.TextField()
    title = models.TextField()
    keywords = models.TextField()
    opt_id = models.TextField()
    saved = models.BooleanField(default=False)

    def __str__(self):
        return self.title


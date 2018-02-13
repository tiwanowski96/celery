from django.db import models

class Website(models.Model):
    url = models.URLField(max_length=128, unique=True)
    title = models.CharField(max_length=128, null=True)
    alexa_rank = models.IntegerField(null=True, blank=True, default=0)
    category = models.ForeignKey('WebsiteCategory', null=True)
    date_added = models.DateField(auto_now_add=True)
    date_updated = models.DateField(auto_now=True)

    def __str__(self):
        return self.title


class WebsiteCategory(models.Model):
    name = models.CharField(max_length=128)
    description = models.CharField(max_length=128)
    date_added = models.DateField(auto_now_add=True)
    date_updated = models.DateField(auto_now=True)
    count = models.IntegerField(null=True)

    def __str__(self):
        return self.name


class WebsitePage(models.Model):
    website = models.ForeignKey(Website)
    url = models.URLField(max_length=128)
    date_added = models.DateField(auto_now_add=True)
    date_updated = models.DateField(auto_now=True)
    title = models.CharField(max_length=128, null=True, blank=True)

    def __str__(self):
        return self.title


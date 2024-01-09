from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from django.db.models.signals import pre_save, post_save
from django.db.models import Q
# Create your models here.


class ArticleQuerySet(models.QuerySet):
    def search (self, query=None):
        if query is None or query == "":
            return self.all()
        try:
            int(query)
        except:
            lookups = Q(title__icontains=query)
        else:
            lookups = Q(title__icontains=query) | Q(id=query)
        return self.filter(lookups)


class ArticleManager(models.Manager):

    def get_queryset(self):
        return ArticleQuerySet(self.model, using=self._db)

    def search(self, query=None):
        return self.get_queryset().search(query)


class Article(models.Model):
    title = models.CharField(max_length=225)
    content = models.TextField()
    image = models.ImageField(upload_to='articles/', null=True,)
    created_date = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(null=True, unique=True, blank=True)

    objects = ArticleManager()

    def __str__(self):
        return self.title

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        if self.slug is None:
            self.slug = slugify(self.title)
        super().save(force_insert=False, force_update=False, using=None, update_fields=None)

    # @property
    # def get_absolute_url(self):
    #     return reverse('article:detail', args=[self.id])


def article_pre_save(sender, instance, *args, **kwargs):
    instance.slug = slugify(instance.title)
    if Article.objects.filter(slug=slugify(instance.title)).exclude(id=instance.id).exists():
        import uuid
        instance.slug += f"-{uuid.uuid4()}"



def article_post_save(sender, instance, created, *args, **kwargs):
    if created:
        instance.slug = slugify(instance.title)
        instance.save()

pre_save.connect(article_pre_save, sender=Article)
# post_save.connect(article_post_save, sender=Article)

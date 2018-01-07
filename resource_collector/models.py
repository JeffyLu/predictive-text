from django.db import models


class Article(models.Model):

    source_url = models.CharField(max_length=255)
    source_url_hash = models.CharField(max_length=32, unique=True)
    is_used = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def article_content(self):
        try:
            ac = ArticleContent.objects.get(article_id=self.pk)
        except ArticleContent.DoesNotExist:
            return ''
        return ac.content


class ArticleContent(models.Model):

    article_id = models.BigIntegerField(unique=True)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
